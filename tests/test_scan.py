import main
from models import ScanRecord
from backend import ScanEngineError

def test_scan_without_key_returns_401(client):
    response = client.post("/scan", json={"raw_code": "hi"})
    assert response.status_code == 401

def test_scan_with_wrong_key_returns_401(client):
    response = client.post(
        "/scan",
        json={"raw_code": "hi"},
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 401 

def test_clean_scan_saves_none_risk(client, db_session, monkeypatch):
    # Fake Gemini: always says "nothing found"
    monkeypatch.setattr(
        main, "scan_code_for_secrets",
        lambda code: {"sanitized_code": code, "threat_summary": []},
    )

    response = client.post(
        "/scan",
        json={"raw_code": "hello"},
        headers={"X-API-Key": "test-api-key"},
    )

    assert response.status_code == 200
    record = db_session.query(ScanRecord).one()
    assert record.has_secrets == "No"
    assert record.risk_level == "None"  

def test_worst_severity_saved_and_raw_secret_not_stored(client, db_session, monkeypatch):
    fake_report = {
        "sanitized_code": "PASSWORD = [REDACTED]",
        "threat_summary": [
            {"type": "IP Address", "count": 1, "severity": "MEDIUM"},
            {"type": "Password", "count": 1, "severity": "CRITICAL"},
        ],
    }
    monkeypatch.setattr(main, "scan_code_for_secrets", lambda code: fake_report)

    response = client.post(
        "/scan",
        json={"raw_code": "PASSWORD = 'SuperSecret123!'"},
        headers={"X-API-Key": "test-api-key"},
    )

    assert response.status_code == 200
    record = db_session.query(ScanRecord).one()
    assert record.has_secrets == "Yes"
    assert record.risk_level == "CRITICAL"          # worst of MEDIUM and CRITICAL
    assert "SuperSecret123!" not in record.submitted_code
    assert "SuperSecret123!" not in record.raw_report


def test_engine_failure_returns_503_and_saves_nothing(client, db_session, monkeypatch):
    def broken_scan(code):
        raise ScanEngineError("gemini down")

    monkeypatch.setattr(main, "scan_code_for_secrets", broken_scan)

    response = client.post(
        "/scan",
        json={"raw_code": "hello"},
        headers={"X-API-Key": "test-api-key"},
    )

    assert response.status_code == 503
    assert db_session.query(ScanRecord).count() == 0    
