import time
import sys
from platform import system
from os import system as command
if system() == "Windows": 
    from msvcrt import getch
else:
    from tty import setcbreak

def cls():
    if system() == "Windows":
        command("cls")
    else:
        command("clear")

def choose_role():
    if system() == "Windows":

        char = str(getch())[2]

        while char != "1" and char != "2" and char != "0":
            print("\nInvalid input. Please try again.")
            char = str(getch())[2]

        if char == "1":
            pass

        elif char == "2":
            pass

        elif char == "0":
            exit()
        
    else:
        setcbreak(sys.stdin)
        char = sys.stdin.read(1)

        while char != "1" and char != "2" and char != "0":
            print("\nInvalid input. Please try again.")
            char = sys.stdin.read(1)

        if char == "1":
            pass
        
        elif char == "2":
            pass

        elif char == "0":
            exit()
    cls()
    
cls()
print("\nWelcom to Bike Rental System!", end="")
time.sleep(3)
cls()

t = 0
print("\nSystem is starting", end="")

while t<3:
    print(".", flush=True, end="")
    t+=1
    time.sleep(2)

time.sleep(1)
cls()

print("\n1. Admin")
time.sleep(0.25)
print("2. User")
time.sleep(0.25)
print("0. Exit")

choose_role()

