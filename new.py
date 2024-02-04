import sqlite3
from tabulate import tabulate
import time
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
    0. Logout"""

USER_MENU = """
\033[1;34mUSER PAGE\033[0m
    1. Available Bikes
    2. Rented Bikes
    3. Return Bike
    4. Rent a Bike!
    5. List of Bikes
    0. Logout"""


connection = sqlite3.connect("DB.db")
cursor = connection.cursor()

QUERY = """CREATE TABLE IF NOT EXISTS users
(
username TEXT,
password TEXT,
role TEXT,
renting TEXT 
);"""
cursor.execute(QUERY)
connection.commit()

QUERY = """CREATE TABLE IF NOT EXISTS bikes
    (
    SN TEXT,
    renter TEXT
    );"""
cursor.execute(QUERY)
connection.commit()


def getchar():
    if system() == "Windows":

        char = str(getch())[2]
    else:
        setcbreak(sys.stdin)
        char = sys.stdin.read(1)

    return char

def cls():
    if system() == "Windows":
        command("cls")
    else:
        command("clear")

def check_repeated(table, column, value):
    cursor.execute("SELECT * FROM {} WHERE {} = ?".format(table, column), (value,))
    row = cursor.fetchone()
    if row is not None:
        return True
    else:
        return False

def SignUp():
    print(HEADER)
    print("\n\33[1;34mAdd new User\33[0m")

    username = input("Username: ")
    password = input("Password: ")

    if check_repeated("users", "username", username):
        return [0, username]

    else:
        return [1, username, password]

def check_role(username, password):
    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
    role = cursor.fetchone()
    if role is None:
        return -1
    elif role[0] == "admin":
        return 1
    elif role[0] == "user":
        return 0

def Login(char):
    username = input("Username: ")
    password = input("Password: ")

    if char == '3' and check_role(username, password) != 1:
        return [0, username]

    else:
        return [1, username, password]

class Bike:
    def __init__(self, SN):
        self.SN = SN
        self.renter = None

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.role = "None"

class Normal(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.role = "user"
    
    def available_bikes(self):
        print(HEADER)
        print("\n\33[1;34mList of Available Bikes\33[0m")

        cur = cursor.execute('SELECT SN FROM bikes WHERE renter = "None"')
        rows = cur.fetchall()

        print(tabulate(rows, headers=[description[0] for description in cur.description], tablefmt="grid"))
        return rows

    def My_Bikes(self):
        print(HEADER)
        print("\n\33[1;34mList of My Bikes\33[0m")

        cur = cursor.execute('SELECT renting FROM users WHERE username = ?', (self.username,))
        rows = cur.fetchall()
        print(tabulate(rows, headers=[description[0] for description in cur.description], tablefmt="grid"))
        return rows
        #print("\nPress any key to go back...")
        #getchar()

    def return_bike(self):
        SNs = self.My_Bikes()
        SNs = SNs[0][0].split(" ")
        SNs.remove("")
        #print(SNs)
        serial = input("\nPress ENTER to exit\nor enter your bike Serial Number to return: ")

        while serial:

            if serial in SNs:
                cursor.execute('UPDATE bikes SET renter = ? WHERE SN = ?', ("None", serial))

            
                cur = cursor.execute('SELECT renting FROM users WHERE username = ?', (self.username,))
                rows = cur.fetchall()[0][0]
                rows = rows.split(" ")
                rows.remove(serial)

                #print(rows)
                #getchar()

                rows = " ".join(rows)
                #print(rows)
                #getchar()

                cursor.execute('UPDATE users SET renting = ? WHERE username = ?', (rows, self.username))
                
                connection.commit()
                
                cls()
                SNs = self.My_Bikes()
                SNs = SNs[0][0].split(" ")
                SNs.remove("")

                #print(SNs)
                
                print("\nBike Returned Successfully!")
                serial = input("\nPress ENTER to exit\nor enter your bike Serial Number to return: ")
            else:
                print("\nInvalid Serial Number. Please try again.")
                serial = input("\nPress ENTER to exit\nor enter your bike Serial Number to return: ")

        connection.commit()

    def rent_bike(self): #There is a Three bikes limit for every single user
        SNs = self.My_Bikes()
        SNs = SNs[0][0].split(" ")
        SNs.remove("")
        #print("RENTED TEST => ", SNs)
        cls()

        available = self.available_bikes()
        available = [row[0] for row in available]
        serial = input("\nPress ENTER to exit\nor enter your bike Serial Number to rent: \n")
        #print("\n[TEST] ", serial in available, " [available : ] ", available, " [self.Serisal :] ",serial)
        #getchar()

        while serial:

            if len(SNs) == 3:
                cls()
                print("\n\033[1;31m\033[1mYou have reached the limit of three bikes.\nPlease return one of your bikes to rent another.\033[0m\nPress Enter to open \"Return Bikes\" Menu...")
                time.sleep(5)
                getchar()
                cls()
                self.return_bike()
                break

            elif serial in available:
                #print('UPDATE bikes SET renter = ? WHERE SN = ?', (self.username, serial))
                #getchar()
                cursor.execute('UPDATE bikes SET renter = ? WHERE SN = ?', (self.username, serial))
                connection.commit()
                

                cur = cursor.execute('SELECT renting FROM users WHERE username = ?', (self.username,))
                rows = cur.fetchall()[0][0]
                rows = rows + " " + serial

                #print(rows)
                #getchar()

                cursor.execute('UPDATE users SET renting = ? WHERE username = ?', (rows, self.username))
                connection.commit()

                cls()
                SNs = self.My_Bikes()
                SNs = SNs[0][0].split(" ")
                SNs.remove("")
                cls()

                available = self.available_bikes()
                available = [row[0] for row in available]

                print("\nBike Rented Successfully!")
                serial = input("\nPress ENTER to exit\nor enter your bike Serial Number to rent: ")
            else:
                cls()
                self.available_bikes()
                print("\nInvalid Serial Number. Please try again.")
                serial = input("\nPress ENTER to exit\nor enter your bike Serial Number to rent: ")

    def list_bikes(self):
        print(HEADER)
        print("\n\33[1;34mList of Bikes\33[0m")

        cur = cursor.execute('SELECT SN FROM bikes')
        rows = cur.fetchall()

        print(tabulate(rows, headers=[description[0] for description in cur.description], tablefmt="grid"))
        print("\nPress any key to go back...")

        getchar()


def first_admin():
    print(HEADER)
    print("\n\33[1;34mAdd new Admin\33[0m")
    username = input("Username: ")
    password = input("Password: ")
    role = "admin"
    renting = ""

    cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (username, password, role, renting))
    connection.commit()
    print("\033[96m\nAdmin Added Successfully!\033[0m\u2705")

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.role = "Admin"

    def add_bike(self):

        print(HEADER)
        # List Of ALL BIKES should be ADDED HERE

        print("\n\33[1;34mAdd new Bike\33[0m")
        serial = input("Serial Number: ")
        
        if check_repeated("bikes", "SN", serial):
            print("Bike Serial Number already exists. Exiting...")
            time.sleep(3)
            pass                                                      #TOdO: fix this

        else:
            bike = Bike(serial)
            bike.renter = "None"

            cursor.execute("INSERT INTO bikes VALUES(?, ?)", (bike.SN, bike.renter))
            connection.commit()
            print("\033[96m\n Bike Added Successfully!\033[0m\u2705")

    def list_users(self):
        print(HEADER)
        print("\n\33[1;34mList of Users\33[0m")

        cur = cursor.execute('SELECT username, role FROM users')
        rows = cur.fetchall()

        print(tabulate(rows, headers=[description[0] for description in cur.description], tablefmt="grid"))

        print("\nPress any key to go back...")
        getchar()

    def list_bikes(self):
        print(HEADER)
        print("\n\33[1;34mList of Bikes\33[0m")

        cur = cursor.execute('SELECT * FROM bikes')
        rows = cur.fetchall()

        print(tabulate(rows, headers=[description[0] for description in cur.description], tablefmt="grid"))
        print("\nPress any key to go back...")

        getchar()


class Main:

    def __init__(self):
        self.check_admins()


    def choose_role(self):

        char = getchar()

        c = 0
        while char != "1" and char != "2" and char != "3" and char != "0":
            if c == 0:
                print("\nInvalid input. Please try again.")
                char = getchar()
                c = 1
            elif c == 3:
                print("\033[1;31mToo many attempts. Exiting...\033[0m")
                self.cursor.close()
                self.connection.close()
                exit()
            else:
                char = getchar()
                c += 1

        if char == "1" or char == "3":
            cls()
            loginData = Login(char)
            if loginData[0] == 0:
                print(f"\n\033[1;31m{loginData[1]} is NOT Admin !\033[0m\n")
                time.sleep(3)
                cls()
                self.Logout()
            
            elif loginData[0] == 1:

                if check_role(loginData[1], loginData[2]) == 0:
                    user = Normal(loginData[1], loginData[2])
                    cls()
                    self.User_Menu(user)

                elif check_role(loginData[1], loginData[2]) == 1:
                    user = Admin(loginData[1], loginData[2])
                    cls()
                    self.Admin_Menu(user)

                elif check_role(loginData[1], loginData[2]) == -1:
                    cls()
                    print("\n\033[1;31mUser Not Found!\033[0m\nWant to sign up? (y/n)")
                    char = getchar()
                    if char == "y" or char == "Y":
                        cls()
                        data = SignUp()

                        if data[0] == 0:
                            print(f"\n\"{data[1]}\"already exists. Exiting...")
                            time.sleep(3)
                            cls()
                            self.Guest_Page()

                        elif data[0] == 1:
                            cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (data[1], data[2], "user", ""))
                            connection.commit()
                            print("\n\033[96mUser Added Successfully!\033[0m\u2705")
                            time.sleep(1.5)

                            print("Please Login Again...")
                            time.sleep(3)
                            cls()
                            self.Guest_Page()

                    elif char == "n" or char == "N":
                        cls()
                        self.Guest_Page()

                    else:
                        cls()
                        print("\nInvalid input. Exiting...")
                        time.sleep(2)
                        self.Logout()

        elif char == "2":
            cls()
            data = SignUp()

            if data[0] == 0:
                print(f"\n\"{data[1]}\"already exists. Exiting...")
                time.sleep(3)
                cls()
                self.Guest_Page()

            elif data[0] == 1:
                cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (data[1], data[2], "user", ""))
                connection.commit()
                print("\n\033[96mUser Added Successfully!\033[0m\u2705")

                print("Please Login Again...")
                time.sleep(3)
                cls()
                self.Guest_Page()

        elif char == "0":
            cls()
            cursor.close()
            connection.close()
            exit()


    def Add_Admin(self):
        print(HEADER)
        print("\n\33[1;34mAdd new Admin\33[0m")
        username = input("Username: ")
        password = input("Password: ")

        if check_repeated("users", "username", username):
            print("\nUser already exists. Exiting...")
            time.sleep(3)
            pass                                                      #TODO: fix this
        else:
            cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (username, password, "admin", ""))
            connection.commit()
            print("\033[96m\nAdmin Added Successfully!\033[0m\u2705")

    def check_admins(self):
        cursor.execute("SELECT * FROM users WHERE role = 'admin'")
        count = cursor.fetchone()
        if count is None:
            cls()
            print("\033[1mOhh, Looks like it's your first time here. \nLet's add an admin...\n")
            time.sleep(3)
            first_admin()

    def User_Menu(self, user):
                                    #TODO : complete this
        print(HEADER)
        print(USER_MENU)
        char = getchar()

        c = 0
        while char != "1" and char != "2" and char != "3" and char != "4" and char != "5" and char != "0":
            if c == 0:
                print("\nInvalid input. Please try again.")
                char = getchar()
                c = 1
            elif c == 3:
                print("\033[1;31mToo many attempts. Exiting...\033[0m")
                self.cursor.close()
                self.connection.close()
                exit()
            else:
                char = getchar()
                c += 1
        match char:
            case '1':
                cls()
                user.available_bikes()
                print("\nPress any key to go back...")
                getchar()
                #time.sleep(3)
                cls()
                self.User_Menu(user)
            case '2':
                cls()
                user.My_Bikes()
                print("\nPress any key to go back...")
                getchar()
                #time.sleep(3)
                cls()
                self.User_Menu(user)
            case '3':
                cls()
                user.return_bike()
                #time.sleep(3)
                cls()
                self.User_Menu(user)
            case '4':
                cls()
                user.rent_bike()
                #time.sleep(20)
                #cls()
                self.User_Menu(user)
            case '5':
                cls()
                user.list_bikes()
                #time.sleep(3)
                cls()
                self.User_Menu(user)
            case '0':
                self.Logout()

    def Admin_Menu(self, user):
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
                self.cursor.close()
                self.connection.close()
                exit()
            else:
                char = getchar()
                c += 1
        match char:
            case "1":
                cls()
                user.add_bike()
                time.sleep(3)
                cls()
                self.Admin_Menu(user)
            case "2":
                cls()
                self.Add_Admin()
                time.sleep(4)
                cls()
                self.Admin_Menu(user)
            case "3":
                cls()
                data = SignUp()

                if data[0] == 0:
                    print(f"\n\"{data[1]}\"already exists. Exiting...")
                    time.sleep(3)
                    cls()
                    self.Guest_Page()

                elif data[0] == 1:
                    cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (data[1], data[2], "user", ""))
                    connection.commit()
                    print("\n\033[96mUser Added Successfully!\033[0m\u2705")
                    time.sleep(1.5)
                    cls()
                    self.Admin_Menu(user)

            case "4":
                cls()
                user.list_users()
                #time.sleep(3)
                cls()
                self.Admin_Menu(user)

            case "5":
                cls()
                user.list_bikes()
                #time.sleep(3)
                cls()
                self.Admin_Menu(user)
            
#            case "6":
#                cls()
#                print("\nLoad Data")
#                time.sleep(3)
#                cls()
#                self.Admin_Menu(user)
            case "0":
                self.Logout()



    def Guest_Page(self):
        cls()
        print(HEADER)
        print("\n1. User Login", end=" || ")
        time.sleep(0.25)
        print("2. Sign Up\n")
        time.sleep(0.25)
        print("3. (I'm ADMIN)", end=" || ")
        time.sleep(0.25)
        print("0. Exit")
        self.choose_role()

    def start(self):
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

        self.Guest_Page()

    def Logout(self):
        print("\Logging out...")
        time.sleep(1)
        cls()
        self.Guest_Page()


def main():
    starter = Main()
    starter.start()

main()
