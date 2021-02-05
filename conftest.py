"""This particular method of fixtures for configuring the test cases
in test_pydango_sqlite.py come from a stack overflow post:
https://stackoverflow.com/questions/58660378/how-use-pytest-to-unit-test-sqlalchemy-orm-classes 
with the solution from user Tryph"""

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from pydango.tables import Base


def pytest_addoption(parser):
    """Argument Parser for pytest"""
    # $ pytest --dburl <name_of_test_database_url>
    parser.addoption('--dburl',
        action='store',
        default='sqlite:///test_pydango.db',
        help='SQLite test database url')
    

@pytest.fixture(scope='session')
def db_engine(request):
    """Get test DB engine"""
    db_url = request.config.getoption("--dburl")
    engine_ = create_engine(db_url, echo=True)
    Base.metadata.create_all(engine_)

    yield engine_

    engine_.dispose()

@pytest.fixture(scope='session')
def db_session_factory(db_engine):
    """returns SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=db_engine))

@pytest.fixture(scope='function')
def db_session(db_session_factory):
    """Yields an SQLAlchemy connection which is rolled-back after the test"""
    session_ = db_session_factory()

    yield session_

    session_.rollback()
    session_.close()





