# 🛡️ CodeShield - Enterprise Data Loss Prevention (DLP)

CodeShield is an AI-powered static code analysis microservice designed to intercept, detect, and redact hardcoded secrets, API keys, and database credentials before they can be pushed to production. 

This project evolved from a monolithic script into a fully decoupled, database-backed microservice architecture capable of handling third-party API timeouts and maintaining permanent threat intelligence logs.

## 🏗️ System Architecture

CodeShield is built on a modern Python microservice stack:

* **Backend Engine:** `FastAPI` (Asynchronous API endpoints)
* **AI Brain:** `Google Gemini 1.5 Flash API` (Prompt-engineered for zero-shot secret detection)
* **Database Vault:** `SQLite` with `SQLAlchemy` ORM (Permanent scan logging)
* **Frontend Client:** `Streamlit` (Decoupled, interactive vulnerability dashboard)

### The Microservice Pipeline
1. The Streamlit Client captures the user's source code and sends an HTTP POST payload to the backend.
2. FastAPI receives the payload and securely interfaces with the Gemini AI engine.
3. The AI categorizes threats by severity (CRITICAL, HIGH) and sanitizes the code.
4. The backend evaluates the threat list, logs the raw data into the SQLite vault, and returns the status to the frontend.
5. The Streamlit dashboard renders the threat metrics and the safe, redacted code.

## ✨ Advanced Features & Resiliency

* **Graceful Degradation (503 Catcher):** If the Google Gemini API experiences high traffic or goes offline, the FastAPI engine catches the HTTP 503 error, safely aborts the scan, and generates a fallback response to prevent server crashes.
* **Silent Failure Prevention:** The UI features strict verification logic to ensure an aborted API call is never falsely reported as a "Clean" scan to the user.
* **Live System Polling:** The frontend actively pings the backend engine to display real-time connection status.

## 🚀 How to Run Locally

Because this is a microservice architecture, the backend and frontend must be run simultaneously in separate terminals.

**1. Clone the repository and activate your environment**
```bash
git clone [https://github.com/your-username/codeshield.git](https://github.com/your-username/codeshield.git)
cd codeshield
env\Scripts\Activate
