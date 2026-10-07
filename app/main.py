from fastapi import FastAPI, Request, HTTPException, status
from app.middleware import verify_hmac_signature
from app.schemas import WebhookPayload
import httpx

app = FastAPI(title="Cloud-Native Webhook & API Security Gateway", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "gateway": "active"}

@app.post("/gateway/webhook", dependencies=[Depends(verify_hmac_signature)])
async def process_webhook(payload: WebhookPayload, request: Request):
    # Stub for HMAC verification & rate limiting (to be added on Days 3 & 4)
    client_ip = request.client.host
    
    # Simulate forwarding valid request to downstream backend
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(f"{settings.TARGET_BACKEND_URL}/webhook", json=payload.model_dump())
    
    return {
        "status": "success",
        "message": "Payload passed HMAC verification and schema validation successfully.",
        "client_ip": client_ip,
        "event_id": payload.event_id
    }