"""Primary function used by pydango.main"""

import os
import random
import string

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from sqlalchemy.orm import sessionmaker
from pydango import connection

from pydango import (
    state
)

from pydango.tables import (
    Account,
    Actor,
    Category,
    Director,
    Movie,
    Theater,
)

from pydango.init_data import (
    accounts_list,
    actors_list,
    categories_list,
    directors_list,
    movies_list,
    theaters_list,
)

def chunks(lst, chunk_size):
    """Generator for movies list"""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def random_number_generator(size=6, chars=string.digits):
    """Generate random numbers to use for payment ids""" 
    return ''.join(random.choice(chars) for _ in range(size))

def yearsago(years, from_date=None):
    """Helper function for calculating the date n years ago
    To be used for receive_before_actor_attach function
    To calculate age of actor"""
    if from_date is None:
        from_date = date.today()
    return from_date - relativedelta(years=years)

def num_years(begin, end=None):
    """Helper function for calculating the date n years ago
    To be used for receive_before_actor_attach function
    To calculate age of actor"""
    if end is None:
        end = date.today()
    num_years = int((end - begin).days / 365.25)
    if begin > yearsago(num_years, end):
        return num_years - 1
    else:
        return num_years


def create_session():
    """Helper to create Session() object in __main__.py"""
    engine = connection.create_connection()
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, session

def create_sqlite_session(engine):
    """Helper to create Session() object in __main__.main()
    for sqlite database"""
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, session

def get_action():
    text = '> '
    if state.active_account:
        text = f'{state.active_account.first_name} {state.active_account.last_name}> '
    action = input(text)
    return action.strip().lower()

"""The following functions will add initial data into the database so the user can get
started right away"""

def insert_account_data(session):
    """Insert data for account Table"""
    # First check if there's existing data
    existing_account = session.query(Account).first()
    if existing_account:
        return
    else:
        for i in accounts_list:
            account = Account(
                email=i[0],
                credit_card=i[1],
                password=i[2],
                zip_code=i[3],
                first_name=i[4],
                last_name=i[5]
            )
            session.add(account)
            session.commit()

def insert_actor_data(session):
    """Insert data for actor Table"""
    # First check if there's existing data
    existing_actor = session.query(Actor).first()
    if existing_actor:
        return
    else:
        for i in actors_list:
            actor = Actor(
                first_name=i[0],
                last_name=i[1],
                birth_day=datetime.strptime(i[2], '%Y-%m-%d').date(),
                # Not necessary but for precalculating age from birthday
                age=num_years(datetime.strptime(i[2], '%Y-%m-%d').date()) 
            )
            session.add(actor)
            session.commit()

def insert_category_data(session):
    """Insert data for the Category table which is separate from the side that enters 
    theater data and the cinephile data"""
    # First check if there's existing data
    existing_drama = session.query(Category).first()
    if existing_drama:
        return
    else:
        for cat in categories_list:
            category = Category(category_name=cat)
            session.add(category)
            session.commit()

def insert_director_data(session):
    """Insert data for the Director table"""
    # First check if there's existing data
    existing_director = session.query(Director).first()
    if existing_director:
        return
    else:
        for i in directors_list:
            director = Director(first_name=i[0],
                last_name=i[1])
            session.add(director)
            session.commit()

def insert_movie_data(session):
    """Insert data for the Movie table"""
    # First check if there's existing data
    existing_movie = session.query(Movie).first()
    if existing_movie:
        return
    else:
        for i in movies_list:
            movie = Movie(
                title=i[0],
                year=i[1],
                rating=i[2],
                length_min=i[3],
                description=i[4],
                director_id=i[5],
                category_id=i[6],
                start_date=datetime.strptime(i[7], '%Y-%m-%d').date(),
                end_date=datetime.strptime(i[8], '%Y-%m-%d').date(),
                active=i[9]
            )
            session.add(movie)
            session.commit()

def insert_theater_data(session):
    """Insert data for theater data"""
    # First check for existing data
    existing_theater = session.query(Theater).first()
    if existing_theater:
        return
    else:
        for i in theaters_list:
            theater = Theater(
                name=i[0],
                ticket_price=i[1],
                address=i[2],
                city=i[3],
                home_state=i[4],
                zip_code=i[5],
                open_time=datetime.strptime(i[6], '%H:%M:%S').time(),
                close_time=datetime.strptime(i[7], '%H:%M:%S').time()
            )
            session.add(theater)
            session.commit()





















