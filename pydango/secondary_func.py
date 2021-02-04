"""Some secondary functions used by main()"""

def print_header():
    print("****************** PYDANGO ******************")
    print()
    print("Welcome to Pydango for movies!")
    print("What would you like to do?")
    print()

def find_user_intent():
    print("[t] List a new movie")
    print("[c] Find a movie")
    print()
    choice = input("Are you a [t]heater owner or [c]inephile? ")
    if choice == 't':
        return 'list'
    return 'find'


def unknown_command():
    print("Sorry we didn't understand that command.")

def success_msg(text):
    print(text)

def error_msg(text):
    print(text)


def exit_app():
    print()
    print('bye!')
    raise KeyboardInterrupt()




