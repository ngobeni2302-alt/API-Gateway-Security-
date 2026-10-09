# Cloud-Native Webhook & API Security Gateway

A lightweight, high-performance security proxy and middleware gateway built with FastAPI and Pydantic. It intercepts, cryptographically validates, rate-limits, and sanitizes incoming webhook payloads before forwarding them to downstream microservices, maintaining a persistent audit log of all security events.

---

## Demo Video
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

git clone https://github.com/ngobeni2302-alt/API-Gateway-Security-.git
   cd API-Gateway-Security-

2. Create a Virtual Environment & Install Dependencies

python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

3. Configure Environment Variables

Copy the example environment file and update your secret key:

cp .env.example .env

4. Run the Application

Start the security gateway server using Uvicorn
uvicorn app.main:app --reload --port 8000

URLs to View the Interface in Your Browser
Open your browser and navigate to one of these routes:

Interactive Swagger UI Documentation (Best View)
Plaintext
http://127.0.0.1:8000/docs

Running Tests

Execute the test suite using pytest to verify security middleware functionality:


pytest -v

### Project Architecture


API-Gateway-Security-/
├── app/
│   ├── main.py          # FastAPI application & route definitions
│   ├── config.py        # Environment settings & secret management
│   ├── schemas.py       # Pydantic models & sanitization logic
│   ├── middleware.py    # HMAC verification & rate-limiting middleware
│   └── database.py      # SQLAlchemy models & audit logging
├── tests/
│   └── test_gateway.py  # Automated test suite
├── Dockerfile           # Multi-stage container deployment
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation


5. Docker Containerization
docker build -t api-security-gateway .

Reads the local Dockerfile and builds an isolated container image tagged (-t) as api-security-gateway.

docker run -p 8000:8000 api-security-gateway

Spins up a running container instance from the built image:

-p 8000:8000: Maps port 8000 on your host machine to port 8000 inside the container so you can access the running gateway server at [http://127.0.0.1:8000](http://127.0.0.1:8000).