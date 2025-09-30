"""
shared pytest fixtures for testing
"""

import sys
import os
import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .virtualbank import base


@pytest.fixture(scope="session")
def test_engine():
    """Create an in-memory SQLite engine for testing"""
    engine = create_engine("sqlite:///:memory:", echo=False)
    base.metadata.create_all(engine)
    return engine


@pytest.fixture
def test_db_session(test_engine):
    """Create a database session for testing"""
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def mock_virtualbank_connection():
    """Mock the database connection in virtualbank module"""
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    base.metadata.create_all(test_engine)

    with patch("virtualbank.VB_CONN", test_engine):
        yield test_engine
