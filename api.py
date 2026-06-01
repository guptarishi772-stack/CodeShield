#Writing an API Server for the Backend Code

#We will use fastapi here.

#First We will import the required libraries:-
from fastapi import FastAPI
from pydantic import BaseModel
from backend import scan_code_for_secrets

#Giving name to fastapi server:-
app = FastAPI()

#Writing the way how the data will be used:-
class CodePayLoad(BaseModel):
    raw_code : str

#writing the post request:-
@app.post("/scan")
def scan_endpoint(payload: CodePayLoad):
    #Taking the code from internet and handing it to backend:-
    threat_report = scan_code_for_secrets(payload.raw_code)
    
    #Returning the response JSON gto the internet:-
    return threat_report 
