#!/usr/bin/env python3

import argparse

from sqlalchemy import create_engine

from pydango import (
    cinephile,
    theater_owner,
    cinephile_sqlite,
    theater_owner_sqlite,
)

from pydango.primary_func import (
    create_session,
    create_sqlite_session,
    insert_account_data,
    insert_actor_data,
    insert_category_data,
    insert_director_data,
    insert_movie_data,
    insert_theater_data,
)

from pydango.secondary_func import (
    print_header,
    find_user_intent
)

from pydango.tables import (
    Base
)



def get_args():
    parser = argparse.ArgumentParser(description='Pydango-pip: the installable database')
    parser.add_argument('-d', '--database', metavar='database',
        default='sqlite', help='Provide a database type: SQLite')
    return parser.parse_args()

def main():

    args = get_args()

    if args.database == 'sqlite':
        # Option to use SQLite instead of PostgreSQL
        engine = create_engine('sqlite:///sqlite3.db')
        # sqlite session
        engine, session = create_sqlite_session(engine=engine)

        Base.metadata.create_all(engine)

        # Autoload some data without user/CLI interface
        insert_category_data(session=session)
        insert_director_data(session=session)
        insert_actor_data(session=session)
        insert_account_data(session=session)
        insert_movie_data(session=session)
        insert_theater_data(session=session)

        print_header()

        try:
            while True:
                if find_user_intent() == 'find':
                    cinephile_sqlite.run()
                else:
                    theater_owner_sqlite.run()
        except KeyboardInterrupt:
            return

        session.close()
    else:
        print("\nYou must provide the '-d sqlite' flag to execute this program.\n")
        print("\nFor help:\n")
        print("python -m pydango -h\n")





if __name__ == '__main__':
    main()
















