from typing import Optional

from sqlalchemy.orm import sessionmaker

from pydango import connection
from pydango.tables import Account

from pydango import primary_func



active_account: Optional[Account] = None

def reload_account():
    engine = connection.create_connection()
    Session = sessionmaker(bind=engine)
    session = Session()
    global active_account
    if not active_account:
        return
    active_account = session.query(Account).filter_by(email=active_account.email).first()
    session.close()








