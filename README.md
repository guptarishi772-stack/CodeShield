# CodeShield 🛡️

**An AI-powered Data Loss Prevention (DLP) microservice that detects and redacts sensitive credentials from source code.**

Most developers accidentally leak an API key or database credential at some point. CodeShield is an automated backend engine designed to catch and sanitize those leaks before they hit production or public repositories.

## ⚙️ Core Architecture

This project was built with a strict focus on backend Python architecture, file I/O handling, and API routing. I utilized Streamlit strictly as a rapid-deployment UI wrapper to visualize the data processing.

*   **File Parsing:** Handles direct buffer reads for `.py`, `.env`, and raw text payloads (`app.py`).
*   **AI Threat Detection:** Securely routes payloads through the GenAI (Gemini) API to analyze code against threat signatures (`scanner.py`).
*   **Strict JSON Schemas:** Forces the LLM to output a categorized threat summary (Critical, High, Medium) and a sanitized, redacted codebase.
*   **Decoupled Logic:** The threat scanning logic is isolated from the UI layer, making it modular and extensible.

   
