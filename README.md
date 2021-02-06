# PYDANGO-PIP

[![PyPI version](https://badge.fury.io/py/pydango-pip.svg)](https://badge.fury.io/py/pydango-pip) [![Documentation Status](https://readthedocs.org/projects/pydango-pip/badge/?version=latest)](https://pydango-pip.readthedocs.io/en/latest/?badge=latest)

pydango-pip is a [pip-installable](https://pypi.org/project/pydango-pip/) database schema that aims to mimic a movie ticket reservation database system (i.e. Fandango) through a CLI.

It's important to note that the database represented by the package is only what I think such a system should look like, not what it actually is.

This was done in the spirit of experimentation and learning as a beginner Python programmer.

The inspiration came from a YouTube video by Mike Kennedy where he builds an Air Bnb-like CLI for MongoDB with MongoEngine. I've taken a lot of his code and refactored it for SQLAlchemy and relational databases.  You can find the video here: https://youtu.be/E-1xI85Zog8

You can also find the non-pip-installable version of Pydango called simply "Pydango" here: https://github.com/Captmoonshot/pydango .  

This regular version of Pydango is good to clone and interact with through both the CLI and a database backend to really grokk what goes on behind the scenes.  Once you clone it, and set up a configuration file, you can use it for both an SQLite and/or PostgreSQL database backend.

However, pydango-pip will only work with SQLite database backends.

If you're curious about the actual database design, you can find the full SQL code to create the entire schema with MySQL at the [py-dango GitHub repository](https://github.com/Captmoonshot/py-dango).

## Installation

You can install pydango-pip with pip: [PYPI](https://pypi.org/project/pydango-pip/)

    pip install pydango-pip

pydango-pip is supported by Python 3.7 and above.

## How to use

pydango-pip is a command line application. 

To run:

```$ python -m pydango -d sqlite```

****************** PYDANGO ******************

Welcome to Pydango for movies!
What would you like to do?

[t] List a new movie
[c] Find a movie

`# Choose [C]`

****************** Hello Cinephile ******************

What action would you like to take:
[C]reate an account
[L]ogin to your account
Log[O]ut of your account
[R]eserve a movie ticket
[V]iew your movie ticket
[S]ee list of available movies
Search for [N]earby theaters
Search by ca[T]egory
[M]ain menu
e[X]it app
[?] Help (this info)

`# Choose [S]`

****************** BROWSE FOR MOVIES ******************


Title: Pulp Fiction | Rating: R
            Description: Boxing, Robbery, Hitmen, Samuel L. Jackson

Title: Jurassic Park | Rating: PG-13
            Description: Dinosaurs, DNA, T-Rex, Velociraptor, Chaos

Title: A Clockwork Orange | Rating: R
            Description: Crazy, Crime, Future, Dystopian

Title: Aliens | Rating: R
            Description: Aliens, Eat People, Spaceship, Future

Title: Interstellar | Rating: PG-13
            Description: Apocalypse, Black Hole, Time Travel, Astronauts

--More--<ENTER>

Personally, building the project allowed me to appreciate what database engineers do for a living, and also to grokk database designs and just how complicated relational databases can get in the wild.

Special shoutout to the [Las Vegas OpenSource Programming Group](https://github.com/OpenSource-Programming/sqlforbeginners) for challenging me to take on this project.

## To test 

Clone the project and run:

`$ tox`


For help:

`$ python -m pydango -h`

