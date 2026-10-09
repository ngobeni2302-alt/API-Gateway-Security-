import hmac
import hashlib
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def generate_signature(payload_dict: dict, secret: str = settings.GATEWAY_SECRET_KEY) -> str:
    body_bytes = json.dumps(payload_dict).encode("utf-8")
    computed_hash = hmac.new(
        key=secret.encode("utf-8"),
        msg=body_bytes,
        digestmod=hashlib.sha256
    ).hexdigest()
    return f"sha256={computed_hash}"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "gateway": "active"}

def test_missing_hmac_signature():
    payload = {
        "event_id": "evt_10001",
        "event_type": "user.signup",
        "timestamp": 1728220800,
        "data": {"user_id": 42}
    }
    response = client.post("/gateway/webhook", json=payload)
    assert response.status_code == 401
    assert "Missing cryptographic signature" in response.json()["detail"]

def test_invalid_hmac_signature():
    payload = {
        "event_id": "evt_10001",
        "event_type": "user.signup",
        "timestamp": 1728220800,
        "data": {"user_id": 42}
    }
    headers = {"X-Hub-Signature-256": "sha256=invalid_hash_string"}
    response = client.post("/gateway/webhook", json=payload, headers=headers)
    assert response.status_code == 401
    assert "Invalid cryptographic signature" in response.json()["detail"]

def test_valid_webhook_request():
    payload = {
        "event_id": "evt_10001",
        "event_type": "user.signup",
        "timestamp": 1728220800,
        "data": {"user_id": 42}
    }
    sig = generate_signature(payload)
    headers = {"X-Hub-Signature-256": sig}
    
    response = client.post("/gateway/webhook", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["event_id"] == "evt_10001"

def test_injection_attempt_in_event_type():
    payload = {
        "event_id": "evt_10002",
        "event_type": "user.signup; DROP TABLE users;--",
        "timestamp": 1728220800,
        "data": {}
    }
    sig = generate_signature(payload)
    headers = {"X-Hub-Signature-256": sig}
    
    response = client.post("/gateway/webhook", json=payload, headers=headers)
    assert response.status_code == 422