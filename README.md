# Cloud-Native Webhook & API Security Gateway

A lightweight, high-performance security proxy and middleware gateway built with FastAPI and Pydantic. It intercepts, cryptographically validates, rate-limits, and sanitizes incoming webhook payloads before forwarding them to downstream microservices, maintaining a persistent audit log of all security events.

---

## 🎥 Demo Video
Watch the 5-minute project walkthrough and live demonstration: 

---

## Key Security Features

1. **HMAC Signature Verification:** Prevents request tampering and forgery by verifying cryptographic signatures (`X-Hub-Signature`).
2. **Strict Schema Validation:** Uses Pydantic to enforce rigid data contracts, rejecting malformed requests or injection attempts with `422` status codes.
3. **IP-Based Rate Limiting:** Throttles abusive clients or automated bot traffic, returning `429 Too Many Requests` when thresholds are breached.
4. **Immutable Audit Logging:** Records every blocked request, timestamp, source IP, and failure reason into a persistent SQLite audit trail.

---

## Tech Stack

* **Framework:** FastAPI (Python)
* **Validation:** Pydantic V2
* **Cryptography:** Python standard `hmac` & `hashlib`
* **Persistence:** SQLite & SQLAlchemy
* **Testing:** Pytest & HTTPX

---

## Getting Started & Installation

1. Clone the Repository

git clone [https://github.com/your-username/api-security-gateway.git](https://github.com/your-username/api-security-gateway.git)

cd api-security-gateway

2. Create a Virtual Environment & Install Dependencies

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

3. Configure Environment Variables

Copy the example environment file and update your secret key:

cp .env.example .env

4. Run the Application
Start the security gateway server using Uvicorn



uvicorn app.main:app --reload --port 8000

Running Tests

Execute the test suite using pytest to verify security middleware functionality:


pytest -v

### Project Architecture


api-security-gateway/
├── app/
│   ├── main.py          # Environment configuration
│   ├── schemas.py       # Pydantic request models
│   ├── middleware.py    # Security & auth logic
│   └── database.py      # SQLite audit log models
├── tests/
│   └── test_gateway.py  # Unit tests for security controls
└── requirements.txt