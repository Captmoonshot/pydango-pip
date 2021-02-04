"""Account class for the account TABLE"""

import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy_utils import (
    PasswordType,
    JSONType
)

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Integer,
    ForeignKey,
    ForeignKeyConstraint,
    Numeric,
    PrimaryKeyConstraint,
    String,
    Table,
    Text,
    Time,
)

Base = declarative_base()

class Account(Base):
    __tablename__ = "account"

    id              = Column(Integer, primary_key=True)
    email           = Column(String(50), nullable=False, unique=True)
    credit_card     = Column(BigInteger, nullable=False)
    # sqlalchemy_utils.PasswordType requires passlib
    # pip install passlib
    password        = Column(PasswordType(
                schemes=[
                    'pbkdf2_sha512',
                    'md5_crypt'
                ],
                deprecated=['md5_crypt']
    ), unique=False, nullable=False)
    zip_code        = Column(Integer, nullable=False)
    first_name      = Column(String(30), nullable=True)
    last_name       = Column(String(30), nullable=True)
    theater_owner   = Column(Boolean, nullable=True)
    created         = Column(DateTime, default=datetime.datetime.now)
    updated         = Column(DateTime, onupdate=datetime.datetime.now)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, email={self.email})>"

# Many-To-Many Through Table for Movie and Actor
movie_actors = Table(
    'movie_actors',
    Base.metadata,
    Column('movie_id', ForeignKey('movie.id'), primary_key=True),
    Column('actor_id', ForeignKey('actor.id'), primary_key=True)
)

class Actor(Base):
    __tablename__ = 'actor'

    id          = Column(Integer, primary_key=True)
    first_name  = Column(String(50), nullable=True)
    last_name   = Column(String(50), nullable=True)
    birth_day   = Column(Date, nullable=True)
    age         = Column(Integer, nullable=True)
    movies      = relationship("Movie",
        secondary=movie_actors,
        back_populates="actors")

    def __repr__(self):
        return f"<{self.__class__.__name__}(first_name={self.first_name}, last_name={self.last_name})>"


class Category(Base):
    __tablename__ = "category"

    id              = Column(Integer, primary_key=True)
    category_name   = Column(String(50), unique=True, nullable=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}(name={self.category_name})>"


class Director(Base):
    __tablename__ = 'director'

    id          = Column(Integer, primary_key=True)
    first_name  = Column(String(50), nullable=True)
    last_name   = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}(first_name={self.first_name}, last_name={self.last_name})>"


class Movie(Base):
    __tablename__ = 'movie'

    id              = Column(Integer, primary_key=True)
    title           = Column(String(50), nullable=False)
    year            = Column(Integer, nullable=True)
    rating          = Column(String(5), nullable=True)
    length_min      = Column(Integer, nullable=True)
    description     = Column(Text, nullable=True)
    director_id     = Column(Integer, ForeignKey(
            'director.id',
            ondelete='CASCADE'
    ))
    director        = relationship("Director", back_populates='movies')
    category_id     = Column(Integer, ForeignKey(
            'category.id',
            ondelete='CASCADE'
    ))
    category        = relationship("Category", back_populates='movies')
    start_date      = Column(Date, nullable=True)
    end_date        = Column(Date, nullable=True)
    active          = Column(Boolean, nullable=True)
    actors          = relationship("Actor",
            secondary=movie_actors,
            back_populates="movies")
    theaters        = relationship("TheaterMovie", back_populates="movie")

    def __repr__(self):
        return f"<{self.__class__.__name__}(title={self.title}, year={self.year})>"

# Reverse relationships for One-to-Many with Movie Table
Director.movies = relationship("Movie", order_by=Movie.id, back_populates="director")
Category.movies = relationship("Movie", order_by=Movie.id, back_populates="category")


class Theater(Base):
    __tablename__ = 'theater'

    id              = Column(Integer, primary_key=True)
    name            = Column(String(50), nullable=False)
    ticket_price    = Column(JSONType, nullable=True)
    address         = Column(String(50), nullable=True)
    city            = Column(String(50), nullable=True)
    home_state      = Column(String(50), nullable=True)
    zip_code        = Column(Integer, nullable=True)
    open_time       = Column(Time, nullable=True)
    close_time      = Column(Time, nullable=True)
    movies          = relationship("TheaterMovie", back_populates="theater")

    def __repr__(self):
        return f"<{self.__class__.__name__}(name={self.name}, address={self.address})>"



class TheaterMovie(Base):
    __tablename__ = 'theatermovie'

    theater_id      = Column(Integer, ForeignKey('theater.id'), primary_key=True)
    movie_id        = Column(Integer, ForeignKey('movie.id'), primary_key=True)
    num_of_screens  = Column(Integer, nullable=True)
    movie           = relationship("Movie", back_populates="theaters")
    theater         = relationship("Theater", back_populates="movies")

    def __repr__(self):
        return f"""<{self.__class__.__name__}(theater_id={self.theater_id},
        movie_id={self.movie_id}, num_of_screens={self.num_of_screens})>"""

# Many-to-Many for Theater and Movie table
# with regular FKs and a Composite PK made of
# theater_id, movie_id, and time fields
# Makes use of SQLAlchemy Expression Language
theater_schedule = Table(
    'theater_schedule',
    Base.metadata,
    Column('theater_id', ForeignKey('theater.id')),
    Column('movie_id', ForeignKey('movie.id')),
    Column('time', Time, nullable=False),
    Column('seats_available', Integer),
    PrimaryKeyConstraint(
        'theater_id',
        'movie_id',
        'time',
        name='theater_schedule_pk'
    )
)


class Payment(Base):
    __tablename__ = 'payment'

    id          = Column(Integer, primary_key=True)
    credit_card = Column(BigInteger, nullable=True)
    paid        = Column(Boolean, nullable=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, paid={self.paid})>"



class Ticket(Base):
    __tablename__ = 'ticket'

    id              = Column(Integer, primary_key=True)
    theater_id      = Column(Integer, nullable=False)
    movie_id        = Column(Integer, nullable=False)
    time            = Column(Time, nullable=False)
    payment_id      = Column(Integer, ForeignKey(
            'payment.id',
            ondelete='CASCADE'
    ))
    payment         = relationship("Payment", back_populates="tickets")
    account_id      = Column(Integer, ForeignKey(
            'account.id',
            ondelete='CASCADE'
    ))
    account         = relationship("Account", back_populates="tickets")
    quantity        = Column(Integer, nullable=False)
    total           = Column(Numeric(6, 2), nullable=False)
    created         = Column(DateTime, default=datetime.datetime.now)
    updated         = Column(DateTime, onupdate=datetime.datetime.now)

    __table_args__  = (ForeignKeyConstraint(
            [theater_id, movie_id, time],
            [theater_schedule.c.theater_id, theater_schedule.c.movie_id, theater_schedule.c.time],
    ), )

    def __repr__(self):
        return f"""{self.__class__.__name__}(id={self.id}, theater_id={self.theater_id}, 
        movie_id={self.movie_id}, time={self.time}, payment_id={self.payment_id}, 
        account_id={self.account_id}, quantity={self.quantity}, total={self.total}, 
        created={self.created}, updated={self.updated})>"""

# Reverse relationships for One-to-Many with Ticket table
theater_schedule.tickets = relationship("Ticket", back_populates="theater_schedule")
Payment.tickets = relationship("Ticket", back_populates="payment")
Account.tickets = relationship("Ticket", back_populates="account")


    


