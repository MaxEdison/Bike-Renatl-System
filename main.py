import sqlite3
import time
from tabulate import tabulate
import sys
from platform import system
from os import system as command
if system() == "Windows":
    from msvcrt import getch
else:
    from tty import setcbreak

HEADER = """ 
\033[34m   __O\033[0m            \033[33m__O\033[0m
\033[30m*\033[0m\033[34m_`\<,_\033[0m \033[30m* * * *\033[0m \033[33m_`\<,_\033[0m\033[30m* *\033[0m
\033[34m(_)/ (_)\033[0m       \033[33m(_)/ (_)\033[0m   \033[1;32mMAX EDISON - BIKE RENTAL SYSTEM\033[0m 
                          \033[4;33mUnder the License of GPL-3.0\033[0m
\033[30m* * * * * * * * * * * * *\033[0m """

ADMIN_MENU = """
\033[1;34mADMIN PAGE\033[0m
    1. Add Bike(s) \U0001F6B2
    2. Add new Admin
    3. Add new User
    4. List of Users
    5. List of Bikes
    6. Load Data
    0. Logout"""

USER_MENU = """
\033[1;34mUSER PAGE\033[0m
    1. Available Bikes
    2. Rented Bikes
    3. Return Bike
    4. Rent a Bike!
    5. List of Bikes
    6. My rent history
    0. Logout"""


connection = sqlite3.connect("DB.db")
cursor = connection.cursor()


def Logout():
    print("\Logging out...")
    time.sleep(1)
    cls()
    Guest_Page()


QUERY = """CREATE TABLE IF NOT EXISTS users
    (
    username TEXT,
    password TEXT,
    role TEXT
    renting TEXT
    );"""
cursor.execute(QUERY)
connection.commit()

QUERY = """CREATE TABLE IF NOT EXISTS bikes
    (
    name TEXT,
    is_rented TEXT
    );"""
cursor.execute(QUERY)
connection.commit()

def cls():
    if system() == "Windows":
        command("cls")
    else:
        command("clear")

def getchar():
    if system() == "Windows":

        char = str(getch())[2]
    else:
        setcbreak(sys.stdin)
        char = sys.stdin.read(1)

    return char


def check_repeated(table, column, value):
    cursor.execute("SELECT * FROM {} WHERE {} = ?".format(table, column), (value,))
    row = cursor.fetchone()
    if row is not None:
        return True
    else:
        return False

def Add_Admin():
    print(HEADER)
    print("\n\33[1;34mAdd new Admin\33[0m")
    username = input("Username: ")
    password = input("Password: ")
    role = "admin"
    if check_repeated("users", "username", username):
        print("\nUser already exists. Exiting...")
        time.sleep(3)
        pass                                                      #TODO: fix this
    else:
        cursor.execute("INSERT INTO users VALUES(?, ?, ?)", (username, password, role))
        connection.commit()
        print("\033[96m\nAdmin Added Successfully!\033[0m\u2705")
        

def check_admins():
    cursor.execute("SELECT * FROM users WHERE role = 'admin'")
    count = cursor.fetchone()
    if count is None:
        cls()
        print("\033[1mOhh, Looks like it's your first time here. \nLet's add one admin...\n")
        time.sleep(3)
        Add_Admin()

check_admins()

def check_role(username, password):
    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
    role = cursor.fetchone()
    if role is None:
        return -1
    elif role[0] == "admin":
        return 1
    elif role[0] == "user":
        return 0
    
def SignUp():
    username = input("Username: ")
    password = input("Password: ")

    if check_repeated("users", "username", username):
        print("\nUser already exists. Exiting...")
        time.sleep(3)
        cls()
        Guest_Page()
    else:
        cursor.execute("INSERT INTO users VALUES(?, ?, ?)", (username, password, "user"))
        connection.commit()
        print("\nUser Added Successfully!")



def My_Bikes(self):
    print(HEADER)
    print("\n\33[1;34mList of My Bikes\33[0m")

    cur = cursor.execute('SELECT renting FROM users WHERE username = ?', (self.username))
    rows = cur.fetchall()
    rows = rows.split(" ")
    print(tabulate(rows, headers=[description[0] for description in cur.description], tablefmt="grid"))

    print("\nPress any key to go back...")
    getchar()


def User_Menu():
                                #TODO : complete this
    print(HEADER)
    print(USER_MENU)
    char = getchar()

    c = 0
    while char != "1" and char != "2" and char != "3" and char != "4" and char != "5" and char != "6" and char != "0":
        if c == 0:
            print("\nInvalid input. Please try again.")
            char = getchar()
            c = 1
        elif c == 3:
            print("\033[1;31mToo many attempts. Exiting...\033[0m")
            cursor.close()
            connection.close()
            exit()
        else:
            char = getchar()
            c += 1
    match char:
        case "1":
            cls()
            print("\nAdd Bike(s)")
            time.sleep(3)
            cls()
            Admin_Menu()
        case "2":
            cls()
            Add_Admin()
            time.sleep(4)
            cls()
            Admin_Menu()
        case "3":
            cls()
            SignUp()
            time.sleep(3)
            cls()
            Admin_Menu()
        case "4":
            cls()
            My_Bikes()
            #time.sleep(3)
            cls()
            Admin_Menu()

        case "5":
            cls()
            print("\nList of Bikes")
            time.sleep(3)
            cls()
            Admin_Menu()
        case "6":
            cls()
            print("\nLoad Data")
            time.sleep(3)
            cls()
            Admin_Menu()
        case "0":
            Logout()


def Login():                            # Use Polymorphism
    username = input("\nUsername: ")
    password = input("Password: ")

    if check_role(username, password) == 0:
        cls()
        User_Menu()
    elif check_role(username, password) == 1:
        cls()
        Admin_Menu()
    elif check_role(username, password) == -1:
        cls()
        print("\n\033[1;31mUser Not Found!\033[0m\nWant to sign up? (y/n)")
        char = getchar()
        if char == "y" or char == "Y":
            cls()
            SignUp()
        elif char == "n" or char == "N":
            cls()
            Guest_Page()
        else:
            cls()
            print("\nInvalid input. Exiting...")
            time.sleep(2)
            Logout()


def choose_role():

    char = getchar()

    c = 0
    while char != "1" and char != "2" and char != "3" and char != "0":
        if c == 0:
            print("\nInvalid input. Please try again.")
            char = getchar()
            c = 1
        elif c == 3:
            print("\033[1;31mToo many attempts. Exiting...\033[0m")
            cursor.close()
            connection.close()
            exit()
        else:
            char = getchar()
            c += 1

    if char == "1" or char == "3":
        cls()
        Login()

    elif char == "2":
        cls()
        SignUp()

    elif char == "0":
        cls()
        cursor.close()
        connection.close()
        exit()

def Guest_Page():
    cls()
    print(HEADER)
    print("\n1. User Login", end=" || ")
    time.sleep(0.25)
    print("2. Sign Up\n")
    time.sleep(0.25)
    print("3. (I'm ADMIN)", end=" || ")
    time.sleep(0.25)
    print("0. Exit")
    choose_role()

def Add_Bike():
    print(HEADER)
    print("\n\33[1;34mAdd new Bike\33[0m")
    username = input("Username: ")
    password = input("Password: ")
    role = "admin"
    if check_repeated("users", "username", username):
        print("\nUser already exists. Exiting...")
        time.sleep(3)
        pass                                                      #TODO: fix this
    else:
        cursor.execute("INSERT INTO users VALUES(?, ?, ?)", (username, password, role))
        connection.commit()
        print("\033[96m\nAdmin Added Successfully!\033[0m\u2705")
        


def list_users():
    print(HEADER)
    print("\n\33[1;34mList of Users\33[0m")

    cur = cursor.execute('SELECT username, role FROM users')
    rows = cur.fetchall()

    print(tabulate(rows, headers=[description[0] for description in cur.description], tablefmt="grid"))

    print("\nPress any key to go back...")
    getchar()

def Admin_Menu():
    print(HEADER)
    print(ADMIN_MENU)
    char = getchar()

    c = 0
    while char != "1" and char != "2" and char != "3" and char != "4" and char != "5" and char != "6" and char != "0":
        if c == 0:
            print("\nInvalid input. Please try again.")
            char = getchar()
            c = 1
        elif c == 3:
            print("\033[1;31mToo many attempts. Exiting...\033[0m")
            cursor.close()
            connection.close()
            exit()
        else:
            char = getchar()
            c += 1
    match char:
        case "1":
            cls()
            print("\nAdd Bike(s)")
            time.sleep(3)
            cls()
            Admin_Menu()
        case "2":
            cls()
            Add_Admin()
            time.sleep(4)
            cls()
            Admin_Menu()
        case "3":
            cls()
            SignUp()
            time.sleep(4)
            cls()
            Admin_Menu()
        case "4":
            cls()
            list_users()
            #time.sleep(3)
            cls()
            Admin_Menu()

        case "5":
            cls()
            print("\nList of Bikes")
            time.sleep(3)
            cls()
            Admin_Menu()
        case "6":
            cls()
            print("\nLoad Data")
            time.sleep(3)
            cls()
            Admin_Menu()
        case "0":
            Logout()

def start():
    cls()
    print("\nWelcom to Bike Rental System!", end="")

    print(HEADER)
    time.sleep(3)
    cls()

    t = 0
    print("\nSystem is starting", end="")

    while t<3:
        print(".", flush=True, end="")
        t+=1
        time.sleep(2)



start()
Guest_Page()
