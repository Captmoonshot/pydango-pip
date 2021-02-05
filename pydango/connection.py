
from sqlalchemy import create_engine

def create_connection():
    """Connect to SQLite through SQLAlchemy"""
    database_url = "sqlite:///sqlite3.db"
    engine = create_engine(database_url)

    return engine



