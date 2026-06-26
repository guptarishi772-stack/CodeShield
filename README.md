# CodeShield: Cloud-Native Data Loss Prevention (DLP) Engine

CodeShield is a cloud-native, AI-powered Data Loss Prevention (DLP) microservice designed to audit code, logs, and text files for sensitive information. By leveraging asynchronous pattern matching and advanced large language model (LLM) heuristics, CodeShield detects, flags, and redacts critical vulnerabilities such as API keys, Personal Identifiable Information (PII), and intellectual property leaks before they hit public repositories or production environments.

The architecture is entirely decoupled into a high-performance backend microservice and a lightweight, responsive web interface.

---

## 🏛️ System Architecture

CodeShield uses a modern, distributed microservice architecture to isolate secrets and ensure high-availability:

```
[ User Browser ] 
       │
       ▼
┌────────────────────────┐
│   Streamlit Frontend   │  (Hosted on Streamlit Cloud)
│     (frontend.py)      │
└───────────┬────────────┘
            │
            │ Asynchronous REST API (POST /scan)
            ▼
┌────────────────────────┐
│    FastAPI Backend     │  (Hosted on Render)
│       (main.py)        │
└───────────┬────────────┘
            ├────────────────────────┐
            ▼                        ▼
┌────────────────────────┐ ┌────────────────────────┐
│   Google Gemini API    │ │     SQLite Engine      │
│  (AI Analysis Engine)  │ │   (Local Audit Log)    │
└────────────────────────┘ └────────────────────────┘

```

* **Frontend (Streamlit):** Serves as a stateless User Interface. It handles user inputs, transmits files securely via API payload blocks, and renders real-time vulnerability dashboards and redact-in-place text.
* **Backend (FastAPI):** Acts as the centralized core intelligence hub. It orchestrates structural analysis, schedules requests, maintains audit logging via SQLite, and manages secure upstream pipeline integrations.
* **Security Isolation:** Highly sensitive operational assets (such as the Google Gemini API key) are stored strictly within the server-side infrastructure vault of the backend, keeping the public-facing client layout completely secure and clear of hardcoded keys.

---

## 🚀 Features

* **Multi-Tier Scan Pipeline:** Combines traditional high-speed regex tracking with deep semantic contextual analysis via AI.
* **Live Risk Classification:** Categorizes vulnerabilities by severity level (Critical, High, Medium, Low).
* **Intelligent Redaction:** Swaps out high-risk items (e.g., `sk-live-...`, database credentials) with safe placeholders inline.
* **Asynchronous Processing:** Long-polling configuration shields the layout from web timeouts during massive data parsing streams.
* **Health Status Instrumentation:** Real-time frontend sidebar ping checks backend engine responsiveness dynamically.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit, Python Requests
* **Backend Framework:** FastAPI, Uvicorn, Pydantic
* **Core Intelligence:** Google Gemini LLM API (`google-generativeai`)
* **Data Tier:** SQLite 3

---

## ⚙️ Local Configuration & Deployment

### Backend Setup

1. Navigate to your backend directory and install dependencies:
```bash
pip install fastapi uvicorn google-generativeai pydantic

```


2. Configure your Environment Variables:
```bash
export GEMINI_API_KEY="your-api-key-here"

```


3. Boot the local Uvicorn development server:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000

```



### Frontend Setup

1. Install client interface dependencies:
```bash
pip install streamlit requests

```


2. Verify your server endpoint path in `frontend.py`:
```python
API_URL = "http://127.0.0.1:8000/scan"

```


3. Run the Streamlit application interface:
```bash
streamlit run frontend.py

```



---

## 🌐 Production Cloud Settings

### 1. Backend Service (Render)

* **Environment Variables:** Add `GEMINI_API_KEY` to the service environment configuration panel.
* **Health Check Endpoint:** Configure the routing manager to watch `/docs` or `/health` to track instance state.

### 2. Frontend App (Streamlit Cloud)

* **Main File Path:** Set directly to `frontend.py`.
* **Timeout Optimization:** Network requests to the backend are built with adaptive threshold handling (`timeout=60`) to gracefully handle server awakening cycles on free-tier computing networks.