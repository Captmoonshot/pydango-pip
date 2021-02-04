#!/usr/bin/env python3

"""tests for pydango"""


import sqlite3


from pydango.tables import (
    Account,
    Actor,
    Category,
    Director,
    Movie,
    Theater,
)
from pydango.primary_func import (
    insert_account_data,
    insert_actor_data,
    insert_category_data,
    insert_director_data,
    insert_movie_data,
    insert_theater_data,
)


def test_add_account(db_session):
    """Add data to account table"""
    # Note: if you add more data to pydango.init_data.accounts_list
    # this test will fail unless you change the test asserts
    insert_account_data(session=db_session)
    test_accounts = db_session.query(Account).all()
    alex = test_accounts[0]

    assert len(test_accounts) == 3
    assert alex.email == 'alex@gmail.com'

def test_add_actor(db_session):
    """Add data to actor table"""
    # Note: if you add more data to pydango.init_data.actors_list
    # this test will fail unless you change the test asserts
    insert_actor_data(session=db_session)
    test_actors = db_session.query(Actor).all()
    tom_hardy = test_actors[0]

    assert len(test_actors) == 8
    assert tom_hardy.last_name == 'Hardy'

def test_add_category(db_session):
    """Add category to category table"""
    # Note: if you add more data to pydango.init_data.categories_list
    # this test will fail unless you change the test asserts
    insert_category_data(session=db_session)
    test_categories = db_session.query(Category).all()
    drama = test_categories[0]

    assert len(test_categories) == 6
    assert drama.category_name == 'Drama'

def test_add_director(db_session):
    """Add director to director table"""
    # Note: if you add more data to pydango.init_data.directors_list
    # this test will fail unless you change the test asserts
    insert_director_data(session=db_session)
    test_directors = db_session.query(Director).all()
    christopher_nolan = test_directors[4]

    assert len(test_directors) == 6
    assert christopher_nolan.last_name == 'Nolan'

def test_add_movie(db_session):
    """Add movie to movie table"""
    # Note: if you add more data to pydango.init_data.movies_list
    # this test will fail unless you change the test asserts
    insert_movie_data(session=db_session)
    test_movies = db_session.query(Movie).all()
    interstellar = test_movies[5]

    assert len(test_movies) == 6
    assert interstellar.title == 'Interstellar'

def test_add_theater(db_session):
    """Add theater to theater table"""
    # Note: if you add more data to pydango.init_data.theaters_list
    # this test will fail unless you change the test asserts
    insert_theater_data(session=db_session)
    test_theaters = db_session.query(Theater).all()
    amc_rainbow = test_theaters[0]

    assert len(test_theaters) == 3
    assert amc_rainbow.name == 'AMC Rainbow'
 








    
