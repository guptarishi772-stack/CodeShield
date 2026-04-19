import os
import json
import certifi # <--- ADD THIS
from dotenv import load_dotenv

# --- FORCE CORRECT SSL CERTIFICATES ---
# Add these two lines right here to bypass Windows environment issues
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

from google import genai

# Load .env file automatically
load_dotenv(override=True)

# --- Configuration ---
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# ... (the rest of your code remains the same) ...

# --- The System Prompt ---
SYSTEM_PROMPT = """
You are CodeShield, an elite cybersecurity auditor and data loss prevention engine.
Your task is to analyze the provided code or text for sensitive data leakage.

You MUST detect and redact the following:
- API keys, secret keys, tokens, and credentials
- Passwords and passphrases (in any format, e.g., password="...", pwd=...)
- Private IP addresses, internal hostnames, and server addresses
- Database connection strings and URIs
- Private cryptographic keys (RSA, SSH, etc.)
- Personally Identifiable Information (PII) like emails, phone numbers

Your response MUST be a single, valid JSON object with exactly two keys:
1. "sanitized_code": A string containing the full original text, with every piece
   of sensitive data replaced by the token [REDACTED]. Do not change anything else.
2. "threat_summary": A list of objects, where each object has:
   - "type": The category of threat found (e.g., "API Key", "Password", "IP Address")
   - "count": The number of that type found
   - "severity": Either "CRITICAL", "HIGH", or "MEDIUM"

If no threats are found, return an empty list for threat_summary.
Return ONLY the JSON object. No markdown, no explanation, no code fences.
"""

def scan_code_for_secrets(raw_code: str) -> dict:
    response = client.models.generate_content(
        model="gemini-3-flash-preview", 
        contents=raw_code,
        config={"system_instruction": SYSTEM_PROMPT}
    )
    result = json.loads(response.text)
    return result


# --- Test ---
TEST_CODE = """
import requests

DB_HOST = "192.168.1.105"
DB_PASSWORD = "SuperSecret_Prod_Pass!99"

STRIPE_SECRET_KEY = "fake-stripe-key-123"
OPENAI_API_KEY = "fake-openai-key-123"

def fetch_user_data(user_id):
    headers = {"Authorization": "Bearer fake-stripe-key-123"}
    response = requests.get(f"https://api.internal.company.com/users/{user_id}", headers=headers)
    return response.json()
"""

if __name__ == "__main__":
    result = scan_code_for_secrets(TEST_CODE)

    print("\n✅ SCAN COMPLETE")
    print("=" * 50)
    print("🔒 SANITIZED CODE:")
    print(result.get("sanitized_code"))
    print("\n📊 THREAT SUMMARY:")
    for threat in result.get("threat_summary", []):
        print(f"  [{threat['severity']}] {threat['type']}: {threat['count']} found")