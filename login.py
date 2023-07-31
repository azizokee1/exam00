from database import *
from login import *

def admin_menu():
    print("Welcome to Onlin Courses ")
    print("\n 1.Add course   ||   2.Show students ")
    answer = int(input("Enter: "))
    if answer == 1:
        add_course()
        admin_menu()
    elif answer == 2:
        show_students()
        admin_menu()
    else:
        print("Try again !")
        admin_menu()
def user_menu(username):
    print("Welcome to Online Courses ")
    print("\n 1.Show courses  ||   2.Join courses  || 3.Show my courses ")
    answer = int(input("Enter: "))
    if answer == 1:
        show_courses()
        user_menu(username)
    elif answer == 2:
        join_course(username)
        user_menu(username)
    elif answer == 3:
        data = show_my_courses(username)
        if not data:
            print('-------You didn\'t join yet --------------\n')
            user_menu(username)
        user_menu(username)
    else:
        print("Try again !")
        user_menu(username)
def menu():
    print("Welcome to Online Courses ")
    print("\n 1.Register   ||   2.Log in  ")
    answer = int(input("Enter: "))
    if answer == 1:
       is_exists()
       menu()
    elif answer == 2:
        username = input("Username: ")
        password=input("Password: ")
        login1 = login(username,password)
        if login1 == 1:
            admin_menu()
        elif login1 == 2:
            user_menu(username)

menu()
    