from datetime import date, datetime
from getpass import getpass

from sqlalchemy import create_engine

from pydango import state
from pydango.switchlang import switch

from pydango import (
    primary_func,
    secondary_func
)

from pydango.primary_func import (
    create_sqlite_session,
    yearsago,
    num_years,
)

from pydango.tables import (
    Account,
    Actor,
    Category,
    Director,
    Movie,
    Theater,
    TheaterMovie,
    theater_schedule,
)

from pydango.cinephile import (
    log_into_account,
    logout,
)

# Unfortunate I could not find a way to get around creating a 
# second connection the sqlite DB here
engine = create_engine('sqlite:///sqlite3.db')
engine, session = create_sqlite_session(engine=engine)


def run():
    print('****************** Hello Theater Owner ******************')
    print()
    
    show_commands()

    while True:
        action = primary_func.get_action()

        with switch(action) as s:
            s.case('c', create_account)
            s.case('l', log_into_account)
            s.case('o', logout)
            s.case('p', create_movie)
            s.case('h', create_theater)
            s.case('e', add_movie_to_existing_theater)
            s.case('s', add_schedule_to_existing_theater)
            s.case('a', create_actor)
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], secondary_func.exit_app)

            s.default(secondary_func.unknown_command)

        
        if action:
            print()

        if s.result == 'change_mode':
            return



def show_commands():
    print('What action would you like to take: ')
    print('[C]reate a theater owner account')
    print('[L]ogin to your account')
    print('Log[O]out of your account')
    print('Create a t[H]eater')
    print('Add movie to [E]xisting theater')
    print('Add [S]chedule to existing theater')
    print('[P]ost a Movie')
    print('Enter [A]ctor Information')
    print('[M]ain menu')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()

def create_account():
    """Violation of DRY principle"""

    print("****************** REGISTER THEATER OWNER ******************")

    print()
    print("Please provide the following information\n")

    email = input("Email (required): ").strip().lower()
    credit_card = input("Credit-card number (required, i.e. 4444333399993333): ").strip()
    credit_card = int(credit_card)
    password = getpass().strip()
    zip_code = input("Zip-code (required): ").strip()
    zip_code = int(zip_code)
    first_name = input("What is your first name? ").strip()
    last_name = input("What is your last name? ").strip()

    old_account = session.query(Account).filter_by(email=email).first()
    if old_account:
        secondary_func.error_msg(f"ERROR: Account with email {email} already exists.")
        return

    account = Account(
        email=email,
        credit_card=credit_card,
        password=password,
        zip_code=zip_code,
        first_name=first_name,
        last_name=last_name,
        theater_owner=True
    )
    session.add(account)

    # Flush
    my_account = session.query(Account).filter_by(email=email).first()

    session.commit()

    state.active_account = account
    secondary_func.success_msg(f"\nCreated new account with id {state.active_account.id}")


def create_actor():
    print("****************** POST AN ACTOR ******************")
    print()

    if not state.active_account:
        secondary_func.error_msg("You must be logged in to post an actor.")
        return
    if not state.active_account.theater_owner == True:
        secondary_func.error_msg("You must be a theater owner to post a new actor.")
        return
    
    print("Provide the following information\n")

    first_name = input("Actor's first name: ").strip()
    last_name = input("Actor's last name: ").strip()
    birth_day = input("Actor's birthday (YYYY-MM-DD): ").strip()
    birth_day = datetime.strptime(birth_day, '%Y-%m-%d').date()
    # calculate age from birth_day using num_years()
    age = num_years(birth_day)

    actor = Actor(
        first_name=first_name,
        last_name=last_name,
        birth_day=birth_day,
        age=age
    )

    session.add(actor)
    session.commit()

    print("\nSuccess!\n")

def create_movie():
    print("****************** POST A NEW MOVIE ******************")
    print()

    if not state.active_account:
        secondary_func.error_msg("You must be logged in to post a movie.")
        return
    if not state.active_account.theater_owner == True:
        secondary_func.error_msg("You must be a theater owner to post a new movie.")
        return

    # Prep Many-To-One relation data
    actors = session.query(Actor).all()
    categories = session.query(Category).all()
    directors = session.query(Director).all()

    print("Provide the following information\n")

    title = input("Title: ").strip()
    year = input("Year: ").strip()
    year = int(year)
    rating = input("Rating: ").strip()
    length_min = input("Length of movie in minutes: ").strip()
    length_min = int(length_min)
    description = input("""Movie description: """)

    if directors:
        print("\nList of available directors: \n")
        for director in directors:
            print(director.first_name, director.last_name)
    print()
    director_first_name = input("Director's first name: ").strip()
    director_last_name = input("Director's last name: ").strip()

    if categories:
        print("\nList of available categories: \n")
        for category in categories:
            print(category.category_name)
    print()
    category_name = input("Movie category: (i.e. Drama)  ").strip()
    start_date = input("Enter the start date: (YYYY-MM-DD) ").strip()
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = input("Enter the end date: (YYYY-MM-DD) ").strip()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    # List all available actors:
    if actors:
        print("\nList of available actors:\n")
        for actor in actors:
            print(actor.first_name, actor.last_name, actor.age)
    print()

    # For Many-To-Many relationship between movies and actors
    main_first_name = input("Enter main actor's first name: ").strip()
    main_last_name = input("Enter main actor's last name: ").strip()
    another_actor = input("Do you wish to enter another actor (Yes or No)? ")
    if another_actor == "Yes" or another_actor == "Y" or another_actor == "yes" or another_actor == "y":
        supporting_first_name = input("Enter supporting actor's first name: ").strip()
        supporting_last_name = input("Enter supporting actor's last name: ").strip()
    else:
        supporting_first_name = None
        supporting_last_name = None   

    def get_active():
        # Emulating an SQL trigger function
        today = date.today()
        if start_date <= today <= end_date:
            return True
        return False

    if supporting_first_name is not None and supporting_last_name is not None:
        supporting_actor = session.query(Actor).filter_by(
            first_name=supporting_first_name,
            last_name=supporting_last_name
        ).first()
    else:
        supporting_actor = None

    main_actor = session.query(Actor).filter_by(
        first_name=main_first_name,
        last_name=main_last_name
    ).first()
        

    # Grab the relevant ids for the ForeignKey relationship
    director = session.query(Director).filter_by(
        first_name=director_first_name,
        last_name=director_last_name
    ).first()

    # Grab the relevant ids for the ForeignKey relationship
    category = session.query(Category).filter_by(
        category_name=category_name
    ).first()

    movie = Movie(
        title=title,
        year=year,
        rating=rating,
        length_min=length_min,
        description=description,
        director_id=director.id,
        category_id=category.id,
        start_date=start_date,
        end_date=end_date,
        active=get_active()
    )
    movie.actors.append(main_actor)
    if supporting_actor is not None:
        movie.actors.append(supporting_actor)

    # Grab the theater objects
    theaters = session.query(Theater).all()

    # For setting M2M relation between Theater and Movie with extra data: Association obj
    t_info = input("\nWould you like to add theater information for the movie (Yes or No)? ").strip()
    while t_info == "Yes" or t_info == "yes" or t_info == "Y" or t_info == "y":
        print("\nList of available theaters\n")
        for theater in theaters:
            print(f"id: {theater.id}, name: {theater.name}, address: {theater.address}")
        theater_id = input("Enter theater id: ").strip()
        theater_id = int(theater_id)
        # Grab the theater object
        theater = session.query(Theater).filter_by(id=theater_id).first()
        if theater:
            num_of_screens = input(f"Enter number of screens for theater for {title}: ").strip()
            num_of_screens = int(num_of_screens)
            movie.theaters.append(TheaterMovie(theater_id=theater.id, num_of_screens=num_of_screens))
            print("\nYour theater has been added!\n")
            t_info = input("Would you like to add another theater (Yes or No)? ").strip()
            while t_info == "No" or t_info == "no" or t_info == "N" or t_info == "n":
                break
        elif theater is None:
            print("That theater does not exist.")
            continue

    session.add(movie)

    session.commit()

    print("\nSucess!\n")


def create_theater():
    print("****************** REGISTER A NEW THEATER ******************")
    print()

    if not state.active_account:
        secondary_func.error_msg("You must be logged in to register a theater.")
        return
    if not state.active_account.theater_owner == True:
        secondary_func.error_msg("You must be a theater owner to register a theater.")
        return

    print("Please provide the following information")

    # For JSON ticket price data
    price_dict = {}

    name = input("Name of your theater: ").strip()
    ticket_q = input("Would you like to add ticket price information (Yes or No)? ").strip()
    while ticket_q == "Yes" or ticket_q == "Y" or ticket_q == "yes" or ticket_q == "y":
        key = input("Enter a price category (i.e. Adult): ").strip()
        value = input(f"Enter the price for {key} (i.e. 5.00): ").strip()
        price_dict[key] = value
        ticket_q = input("Would you like to add more ticket price information? ").strip()
        if ticket_q == "No" or ticket_q == "N" or ticket_q == "no" or ticket_q == "n":
            break
    address = input("Address: ").strip()
    city = input("City: ").strip()
    home_state = input("State: ").strip()
    zip_code = input("Zip-code: ").strip()
    zip_code = int(zip_code)

    open_time = input("Opening time (9:00:00): ").strip()
    open_time = datetime.strptime(open_time, "%H:%M:%S").time()
    close_time = input("Closing time (21:00:00): ").strip()
    close_time = datetime.strptime(close_time, "%H:%M:%S").time()

    theater = Theater(
        name=name,
        ticket_price=price_dict,
        address=address,
        city=city,
        home_state=home_state,
        zip_code=zip_code,
        open_time=open_time,
        close_time=close_time
    )

    session.add(theater)
    session.commit()

    print("\nSuccess!\n")

def add_movie_to_existing_theater():
    print("****************** ADD A MOVIE TO AN EXISTING THEATER ******************")
    print()

    if not state.active_account:
        secondary_func.error_msg("You must be logged in to add a movie to a theater.")
        return
    if not state.active_account.theater_owner == True:
        secondary_func.error_msg("You must be a theater owner to add a movie.")
        return
    
    print("Please provide the following information.")
    # Grab all theater objects
    theaters = session.query(Theater).all()

    while True:
        # Here we're performing multiple queries inside of a loop
        # which makes it inefficient
        print("\nList of available theaters: \n")
        for theater in theaters:
            print(f"Id: {theater.id}, Name: {theater.name}")
        print()
        theater_id = input("\nEnter the theater's Id you want to add movies for: ").strip()
        theater_id = int(theater_id)
        # Grab the chosen theater object
        theater = session.query(Theater).filter_by(id=theater_id).first()
        print("\nList of available movies: \n")
        # Grab all movie objects
        movies = session.query(Movie).all()
        for movie in movies:
            print(f"Id: {movie.id}, Title: {movie.title}")
        movie_id = input(f"Enter the movie's Id you want to add to {theater.name}: ").strip()
        movie_id = int(movie_id)
        # Grab the movie with the id provided
        movie = session.query(Movie).filter_by(id=movie_id).first()
        num_of_screens = input(f"Enter number of screens for movie {movie.title}: ").strip()
        num_of_screens = int(num_of_screens)
        try:
            theater.movies.append(TheaterMovie(theater_id=theater.id, movie_id=movie.id, num_of_screens=num_of_screens))
            session.add(theater)
            session.commit()
        except Exception as e:
            print(e)
        continue_add = input("Would you like to add another movie to an existing theater (Yes or No)? ").strip()
        if continue_add == "No" or continue_add == "no" or continue_add == "N" or continue_add == "n":
            break
        
def add_schedule_to_existing_theater():
    print("****************** ADD A SCHEDULE TO AN EXISTING THEATER ******************")
    print()

    if not state.active_account:
        print("You must be logged in to add a schedule.")
        return
    if not state.active_account.theater_owner == True:
        print("You must be a theater owner to add a schedule.")
        return

    # Grab Theater and Movie objects
    theaters = session.query(Theater).all()
    movies = session.query(Movie).all()

    # Create a connection obj using Expression Language syntax
    conn = engine.connect()
    
    print("Please provide the following information")

    while True:

        print("\nList of available theaters: \n")
        for theater in theaters:
            # If theater.movies collection actually contains data
            if theater.movies:
                print(f"Id: {theater.id}, Name: {theater.name}")
        print()
        theater_id = input("\nEnter theater's Id: ").strip()
        theater_id = int(theater_id)
        theater = session.query(Theater).filter_by(id=theater_id).first()

        print(f"\nList of available movies for {theater.name}: \n")
        for movie in theater.movies:
            print(f"Id: {movie.movie.id}, Title: {movie.movie.title}")
        movie_id = input("\nEnter movie's Id: ").strip()
        movie_id = int(movie_id)
        movie = session.query(Movie).filter_by(id=movie_id).first()
        print()

        time = input("Enter a time for the movie (i.e. 11:00:00): ").strip()
        time = datetime.strptime(time, "%H:%M:%S").time()
        seats_available = input("Enter number of seats available for scheduled movie: ").strip()
        seats_available = int(seats_available)

        this_schedule = session.query(theater_schedule).filter_by(
            theater_id=theater.id,
            movie_id=movie.id,
            time=time
        ).first()
        
        if not this_schedule:
            schedule = theater_schedule.insert().values(
                theater_id=theater.id,
                movie_id=movie.id,
                time=time,
                seats_available=seats_available
            )
            try:
                result = conn.execute(schedule)
            except Exception as e:
                print(e)
        else:
            print("This schedule already exists!")
            break
        more_schedule = input("Would you like to enter another movie theater schedule? ").strip()
        if more_schedule == "No" or more_schedule == "N" or more_schedule == "no" or more_schedule == "n":
            break


    
        
        




    
    


    

     









    










