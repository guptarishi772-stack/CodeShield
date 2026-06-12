# Writing an API Server for the Backend Code

# First We will import the required libraries:-
from fastapi import FastAPI, Depends       # Added Depends for the database
from pydantic import BaseModel
from sqlalchemy.orm import Session         # Added Session for the database
from backend import scan_code_for_secrets

# Import the Plumbing and Blueprint 
import models
from database import engine, get_db

# This line scans models.py and creates codeshield.db when the server starts
models.Base.metadata.create_all(bind=engine)
# ----------------------------------------------

# Giving name to fastapi server:-
app = FastAPI()

# Writing the way how the data will be used:-
class CodePayLoad(BaseModel):
    raw_code: str

# writing the post request:-
# We hand the database "key" to the endpoint using `db: Session = Depends(get_db)`
@app.post("/scan")
def scan_endpoint(payload: CodePayLoad, db: Session = Depends(get_db)):
    
    # Taking the code from internet and handing it to backend:-
    threat_report = scan_code_for_secrets(payload.raw_code)
    
    # The Propulsion System (Saving to Database) 
    # 1. Safely figure out if secrets exist by checking the threat_summary list
    if len(threat_report.get("threat_summary", [])) > 0:
        secrets_found = "Yes"
    else:
        secrets_found = "No"

    # 2. Package the data into the blueprint using our new variable
    new_scan = models.ScanRecord(
        submitted_code=payload.raw_code,
        has_secrets=secrets_found,
        raw_report=str(threat_report),
        risk_level="High"  # Still hardcoded for testing
    )
    
    # 3. Add it to the staging area and permanently save (commit) it
    db.add(new_scan)
    db.commit()
    
    # Returning the response JSON to the internet:-
    return threat_report