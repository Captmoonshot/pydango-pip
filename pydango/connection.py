
from sqlalchemy import create_engine

def create_connection():
    """Connect to postgresql through SQLAlchemy"""
    database_url = "sqlite:///test_pydango.db"
    engine = create_engine(database_url)

    return engine



