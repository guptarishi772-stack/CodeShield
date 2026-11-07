import os
os.environ.setdefault("GEMINI_API_KEY", "test-key")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import main
import models  # noqa: F401
from database import Base, get_db


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    yield session
    session.close()


@pytest.fixture
def client(db_session, monkeypatch):
    def override_get_db():
        yield db_session

    main.app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setenv("API_KEY", "test-api-key")
    main.limiter.enabled = False
    yield TestClient(main.app)
    main.app.dependency_overrides.clear()
    main.limiter.enabled = True