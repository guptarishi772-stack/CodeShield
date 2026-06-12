from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This creates a simple file named codeshield.db in your project folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./codeshield.db"

# SQLite requires a special argument to prevent thread conflicts during web requests
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# This is the dependency your API endpoints will use to talk to the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()