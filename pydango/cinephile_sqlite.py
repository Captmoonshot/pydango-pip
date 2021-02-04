from getpass import getpass
from pprint import pprint

from datetime import datetime

from sqlalchemy import create_engine

from pydango import state
from pydango.switchlang import switch

from pydango import (
    primary_func,
    secondary_func
)
from pydango.primary_func import chunks

from pydango.primary_func import (
    create_sqlite_session,
    random_number_generator,
)

from pydango.tables import (
    Account,
    Category,
    Movie,
    Payment,
    Ticket,
    Theater,
    theater_schedule,
)

from sqlalchemy.sql import (
    update,
    and_,
)

# Unfortunate I could not find a way to get around creating a 
# second connection the sqlite DB here
engine = create_engine('sqlite:///sqlite3.db')
engine, session = create_sqlite_session(engine=engine)

def run():
    print('****************** Hello Cinephile ******************')
    print()
    
    show_commands()

    while True:
        action = primary_func.get_action()

        with switch(action) as s:
            s.case('c', create_account)
            s.case('l', log_into_account)
            s.case('o', logout)
            s.case('s', list_movies)
            s.case('n', browse_by_location)
            s.case('t', browse_by_category)
            s.case('r', purchase_ticket)
            s.case('v', view_ticket)
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], secondary_func.exit_app)

            s.default(secondary_func.unknown_command)

        
        if action:
            print()

        if s.result == 'change_mode':
            return






def show_commands():
    print('What action would you like to take: ')
    print('[C]reate an account')
    print('[L]ogin to your account')
    print('Log[O]ut of your account')
    print('[R]eserve a movie ticket')
    print('[V]iew your movie ticket')
    print('[S]ee list of available movies')
    print('Search for [N]earby theaters')
    print('Search by ca[T]egory')
    print('[M]ain menu')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()

def create_account():
    print("****************** REGISTER ******************")

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
        last_name=last_name
        # exclude theater_owner attribute
    )
    session.add(account)

    # Flush
    my_account = session.query(Account).filter_by(email=email).first()

    session.commit()

    state.active_account = account
    secondary_func.success_msg(f"\nCreated new account with id {state.active_account.id}")

 

def log_into_account():
    print("****************** LOGIN ******************")

    email = input("Email: ").strip()
    password = getpass().strip()

    account = session.query(Account).filter_by(email=email).first()

    if not account:
        secondary_func.error_msg(f"Could not find account with email ({email})")
        return
    elif account.password != password:
        secondary_func.error_msg(f"Password does not match")
        return
    
    state.active_account = account
    secondary_func.success_msg(f"\nYou are now logged in.")
    # To help with testing in the Python shell
    return state.active_account

def logout():
    if state.active_account is None:
        print("You are already logged-out.")
        return
    state.active_account = None
    print("You are logged-out.")

def list_movies():
    print("****************** BROWSE FOR MOVIES ******************")
    print()

    # Grab all Movie objects
    movies = session.query(Movie).filter_by(active=True).all()
    movies_list = [
        i.__dict__.copy()
        for i in movies
    ]
    # movie __dict__ attribute contains _sa_instance_state which isn't useful
    # popped = [i.pop('_sa_instance_state') for i in movies_list]
    # create a movie_chunks generator out of movie_list
    # to generate 3 items at a time
    movie_chunks = chunks(movies_list, 5)
    while True:
        chunked = next(movie_chunks, None)
        if chunked == None:
            print("The End")
            break
        for i in chunked:
            print(f"""\nTitle: {i['title']} | Rating: {i['rating']}
            Description: {i['description']}""")
        more = input("\n--More--<ENTER>\n")
        if not more == "":
            break

def browse_by_location():
    print("****************** BROWSE FOR MOVIES BY LOCATION ******************")
    print()

    zip_code = input("Enter your zipcode: ").strip()
    zip_code = int(zip_code)

    theaters = session.query(Theater).filter_by(zip_code=zip_code).all()
    if not theaters:
        print("There are no theaters in that zip_code.")
        by_city = input("Would you like to search by city (Yes or <ENTER to quit>)? ").strip()
        if by_city == "":
            return
        city = input("Enter your city of residence: ").strip()
        theaters = session.query(Theater).filter_by(city=city).all()
        if not theaters:
            print("Sorry, but there are no open theaters in your city.")
            return
    for i, theater in enumerate(theaters, 1):
        movies = theater.movies
        print(f"""\n{i}. {theater.name} at {theater.address} {theater.zip_code}
        Open: {theater.open_time.strftime('%H:%M:%S')} | Close: {theater.close_time.strftime('%H:%M:%S')}
        Prices: {theater.ticket_price}
        """)
        print(f"\n{theater.name}'s Movies:\n")
        if movies:
            for movie in movies:
                movie = session.query(Movie).filter_by(id=movie.movie_id).first()
                print(f"Title: {movie.title} | Rating: {movie.rating}\n")
        else:
            print("No movies playing currently due to COVID.")
            print("Please check back when we get a government that cares about its people.")

def browse_by_category():
    print("****************** BROWSE FOR MOVIES BY CATEGORY ******************")
    print()

    categories = session.query(Category).all()
    categories_dict = {
        '1': 'Drama',
        '2': 'Action',
        '3': 'Horror',
        '4': 'Scifi',
        '5': 'Romance',
        '6': 'Comedy'
    }

    print("Movie categories: \n")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category.category_name}")
    print()
    category = input("Which category are you interested in (Enter a number): ").strip()
    category = session.query(Category).filter_by(category_name=categories_dict[category]).first()
    movies = category.movies
    print(f"Movies for category: {category.category_name}\n")
    for i, movie in enumerate(movies, 1):
        print(i, movie.title)


def purchase_ticket():
    print("****************** PURCHASE TICKETS ******************")
    print()

    if not state.active_account:
        print("You must be logged in to purchase a ticket.")
        return

    # Get account credentials that were created on registration
    account = state.active_account

    # Grab the theater_schedule objects
    schedules = session.query(theater_schedule).all()

    print("\nMOVIE THEATER SCHEDULES\n")

    # List all available movies and theaters and times
    # with index loop so they can input a number representing an object
    # that will later get mapped to elements of tuples appended to a list
    index = 0
    for i in schedules:
        theater = session.query(Theater).filter_by(id=i.theater_id).first()
        movie = session.query(Movie).filter_by(id=i.movie_id).first()
        index += 1
        print(f"""{index}: {theater.name} {theater.address}, Prices: {theater.ticket_price} 
        {movie.title}, Schedules: {i.time}, Seats: {i.seats_available}\n""")

    ticket_number = input("\nEnter ticket number: ").strip()
    ticket_number  = int(ticket_number) - 1

    quantity = input("How many tickets would you like to purchase: ").strip()
    quantity = int(quantity)

    category = input("Which category of tickets (i.e. Adult/Child): ").strip()
    
    theaters_list = []
    # Creat a tuple of the required information to purchase a ticket
    # along with an index so the user can select a tuple
    for i, x in enumerate(schedules, 1):
        theater = session.query(Theater).filter_by(id=x.theater_id).first()
        movie = session.query(Movie).filter_by(id=x.movie_id).first()
        payment_id = random_number_generator()
        payment_id = int(payment_id)
        tup = (i, theater.id, movie.id, x.time, payment_id, account.id)
        theaters_list.append(tup)


    my_ticket = theaters_list[ticket_number]

    # I need to figure out the price for the category chosen for 
    # this particular theater outside of the loop because we don't want to do this for every theater
    my_theater = session.query(Theater).filter_by(id=my_ticket[1]).first()
    my_movie = session.query(Movie).filter_by(id=my_ticket[2]).first()

    ticket_price = float(my_theater.ticket_price[category])
    total = ticket_price * quantity

    ticket = Ticket(
        theater_id=my_ticket[1],
        movie_id=my_ticket[2],
        time=my_ticket[3],
        payment_id=my_ticket[4],
        account_id=my_ticket[5],
        quantity=quantity,
        total=total
    )
    
    payment = Payment(
        id=my_ticket[4],
        credit_card=account.credit_card,
        paid=True
    )

    session.add(ticket)
    session.add(payment)
    session.commit()

    # I think there's gotta be a better way to do this, but what it's supposed to do
    # is update the value of seats_available in theater_schedule
    # everytime someone purchases a ticket
    my_theater_schedule = session.query(theater_schedule).filter_by(
            theater_id=my_ticket[1],
            movie_id=my_ticket[2],
            time=my_ticket[3]
    ).first()
    new_seats_available = my_theater_schedule.seats_available - quantity
    engine.execute(update(theater_schedule).where(and_(theater_schedule.c.theater_id==my_ticket[1],
        theater_schedule.c.movie_id==my_ticket[2],
        theater_schedule.c.time==my_ticket[3])).values(seats_available=new_seats_available))


    ticket_receipt = session.query(Ticket).filter_by(id=ticket.id).first()

    print("\nYour receipt: \n")
    print(f"""Movie: {my_movie.title} | Location: {my_theater.name} at {my_theater.address} 
    Time: {ticket_receipt.time} | Quantity: {ticket_receipt.quantity} tickets 
    Total Price: ${total} \n

    Payment Id: {payment.id} | Date of Purchase: {ticket_receipt.created.date()}""")

    print("\nEnjoy your movie!\n")

def view_ticket():
    print("****************** VIEW MY CURRENT TICKETS ******************")
    print()

    if not state.active_account:
        print("You must be logged in to view a purchased ticket.")
        return
    
    # Grab account
    account = state.active_account

    # Get account-related tickets
    tickets = session.query(Ticket).filter_by(account_id=account.id).all()

    # If account has no tickets return
    if not tickets:
        return

    # Return only valid tickets - tickets that were purchased today
    today = datetime.today().date()

    print("\nMy Tickets: \n")

    for ticket in tickets:
        if ticket.created.date() == today:
            theater = session.query(Theater).filter_by(id=ticket.theater_id).first()
            movie = session.query(Movie).filter_by(id=ticket.movie_id).first()
            payment = session.query(Payment).filter_by(id=ticket.payment_id).first()
            if not payment.paid:
                status = 'Unpaid'
            status = 'Paid'
            print(f"""
            Movie: {movie.title} | Location: {theater.name} at {theater.address} 
            Time: {ticket.time} | Quantity: {ticket.quantity} tickets 
            Total Price: ${ticket.total} | Status: {status}\n
            Payment Id: {ticket.payment_id} | Date of Purchase: {ticket.created.date()}\n
            """)











