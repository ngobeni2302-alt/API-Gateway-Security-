from fastapi import FastAPI, Request, HTTPException, status
from sqlalchemy.orm import Session
from app.middleware import verify_hmac_signature, rate_limit_middleware
from app.database import SessionLocal, init_db, AuditLog
from app.schemas import WebhookPayload
from fastapi import FastAPI, Request, Depends, HTTPException, status
import httpx

app = FastAPI(title="Cloud-Native Webhook & API Security Gateway", version="1.0.0")

@app.on_event("startup")
def startup_event():
    init_db()  # Initialize the database and create tables if they don't exist

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "gateway": "active"}

@app.post("/gateway/webhook", dependencies=[Depends(verify_hmac_signature), Depends(rate_limit_middleware)])
async def process_webhook(payload: WebhookPayload, request: Request, db: Session = Depends(get_db)):
    # Stub for HMAC verification & rate limiting (to be added on Days 3 & 4)
    client_ip = request.client.host

    # Save successful processing audit log to SQLite
    audit_entry = AuditLog(
        client_ip=client_ip,
        event_id=payload.event_id,
        event_type=payload.event_type,
        status="SUCCESS",
        details="Payload successfully verified, rate-checked, and validated."
    )
    db.add(audit_entry)
    db.commit()

    return {
        "status": "success",
        "message": "Payload passed security gateway, rate limit, and schema validation successfully",
        "client_ip": client_ip,
        "event_id": payload.event_id
    }