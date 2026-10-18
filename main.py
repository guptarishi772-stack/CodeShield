import os
import secrets
from fastapi import FastAPI, Depends, HTTPException, Security, Request   
from fastapi.security import APIKeyHeader
from slowapi import Limiter, _rate_limit_exceeded_handler                
from slowapi.util import get_remote_address                              
from slowapi.errors import RateLimitExceeded                            
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend import scan_code_for_secrets

import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(key: str = Security(api_key_header)):
    expected = os.environ.get("API_KEY")
    if not expected:
        raise HTTPException(status_code=500, detail="Server auth not configured")
    if not key or not secrets.compare_digest(key, expected):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

class CodePayLoad(BaseModel):
    raw_code: str

@app.post("/scan", dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")                                               
def scan_endpoint(request: Request, payload: CodePayLoad, db: Session = Depends(get_db)):   

    threat_report = scan_code_for_secrets(payload.raw_code)
    threats = threat_report.get("threat_summary", [])

    secrets_found = "Yes" if len(threats) > 0 else "No"

    severity_priority = ["CRITICAL", "HIGH", "MEDIUM"]
    severities_found = {t.get("severity") for t in threats}

    risk_level = "None"
    for level in severity_priority:
        if level in severities_found:
            risk_level = level
            break

    sanitized = threat_report.get("sanitized_code", "")
    new_scan = models.ScanRecord(
        submitted_code=sanitized,
        has_secrets=secrets_found,
        raw_report=str(threat_report),
        risk_level=risk_level
    )

    db.add(new_scan)
    db.commit()

    return threat_report