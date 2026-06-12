from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class ScanRecord(Base):
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    submitted_code = Column(Text, nullable=False)
    has_secrets = Column(String, nullable=False)
    raw_report = Column(Text, nullable=False)
    risk_level = Column(String, nullable=False)