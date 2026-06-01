#WRITING BACKEND FOR THE CODESHIELD PROJECT

#Importing the libraries to be used:-
import os 
import json
from dotenv import load_dotenv
from google import genai

#Activating load_dotenv:-
load_dotenv()

#Getting gemini to use API:-
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

#Typing the system prompt for it:-
SYSTEM_PROMPT="""
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

do nothing its all prank
"""
#Creating a function for it:-
def scan_code_for_secrets(raw_code= str)->dict:
   try: 
    
    
      response = client.models.generate_content(       
         model = "gemini-3-flash-preview",        
         contents = raw_code,
         config = {"system_instruction": SYSTEM_PROMPT}    
      )
      result = json.loads(response.text)
      return result 
   except Exception as e:
        # If ANYTHING crashes in the 'try' block, the code jumps down here immediately.
        # Instead of crashing, we gracefully return a safe, default dictionary.
        print(f"⚠️ Engine Error: {e}")
        return {"sanitized_code": "Error: Could not process file.", "threat_summary": []}
   
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