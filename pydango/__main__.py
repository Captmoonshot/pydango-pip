#!/usr/bin/env python3

"""
Pydango-pip is a pip-intallable database schema that you can interact with through a CLI.
The schema is meant to mimic a movie theater reservation system such as Fandango.  

The inspiration came from a YouTube video by Mike Kennedy where he builds an Air Bnb-like CLI 
for MongoDB with MongoEngine. I've taken a lot of his code and refactored it for SQLAlchemy 
and relational databases.  You can find the video here: https://youtu.be/E-1xI85Zog8.

You can also find the non-pip-installable version of Pydango called simply "Pydango" here: https://github.com/Captmoonshot/pydango .  

This regular version of Pydango is good to clone and interact with through both the CLI and a database backend to really grokk what goes on behind the scenes.  Once you clone it, and set up a configuration file, you can use it for both an SQLite and/or PostgreSQL database backend.

However, pydango-pip will only work with SQLite database backends.

"""

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
    """
    Function to parse arguments from the command-line using the argparse module

    :return: arguments
    """
    parser = argparse.ArgumentParser(description='Pydango-pip: the installable database')
    parser.add_argument('-d', '--database', metavar='database',
        default='sqlite', help='Provide a database type: SQLite')
    return parser.parse_args()

def main():
    """
    Pydango-pip's main executable function.  Gets the database argument
    from the command-line.  Using SQLAlchemy's ORM pattern, creates an engine
    and session.  The session is then used to create the database schema:
    tables and relations.

    We then automatically load initial data into those tables using 
    insert_<table_name>_data(session=session) functions.

    We then divide our users into two distinct groups with the find_user_intent function:
    1. cinephile (people who want to watch movies)
    2. theater_owner (people who own movies theaters and supply the movies to watch)

    And execute the CLI flow for the respective user types.
    """

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
















