import hmac
import hashlib
import time
from collections import defaultdict
from fastapi import Request, HTTPException, status
from app.config import settings

# In-memory store tracking request timestamps per client IP: {ip: [timestamp, ...]}
REQUEST_TRACKER = defaultdict(list)

async def verify_hmac_signature(request: Request):
    """
    Validates the cryptographic HMAC-SHA256 signature sent by the webhook sender
    against the raw body bytes and the secret gateway key.
    """
    # Extract the signature header (commonly used by GitHub, Stripe, etc.)
    signature_header = request.headers.get("X-Hub-Signature-256")
    
    if not signature_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing cryptographic signature header (X-Hub-Signature-256)"
        )
    
    # Read the raw body bytes from the incoming request
    body_bytes = await request.body()
    
    # Compute the expected HMAC-SHA256 hash using our secret key
    computed_hash = hmac.new(
        key=settings.GATEWAY_SECRET_KEY.encode("utf-8"),
        msg=body_bytes,
        digestmod=hashlib.sha256
    ).hexdigest()
    
    expected_signature = f"sha256={computed_hash}"
    
    # Securely compare the signatures to prevent timing attacks
    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid cryptographic signature. Request rejected."
        )
    
    return True

async def rate_limit_middleware(request: Request):
    """
    Enforces a strict IP-based request rate limit window to block brute-force/DoS attacks.
    """
    client_ip = request.client.host
    current_time = time.time()
    
    window_start = current_time - settings.RATE_LIMIT_WINDOW_SECONDS
    
    # Filter out timestamps older than the sliding window window
    timestamps = REQUEST_TRACKER[client_ip]
    valid_timestamps = [ts for ts in timestamps if ts > window_start]
    
    if len(valid_timestamps) >= settings.RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Too many requests from this IP."
        )
    
    valid_timestamps.append(current_time)
    REQUEST_TRACKER[client_ip] = valid_timestamps
    return True