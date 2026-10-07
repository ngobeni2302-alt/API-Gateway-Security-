import hmac
import hashlib
from fastapi import Request, HTTPException, status
from app.config import settings

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