# Bike Rental System
A University OOP Project!

## Description
### The general struture of system is smth like this:
    |__Class (main)
        |__Class (Bike)
                |__Class (ElectricBike)
                |__Class (RoadBike)
        |__Class (User)


### details of Class(main):
    `User_menu()` function which should contain the following:
        1. Available Bikes
        2. Rented Bikes
        3. Return Bike
        4. Rent a Bike!
        5. List of Bikes
        6. My rent history
        7. Exit

    `Admin_menu()` function should contain following:
        1. Add Bike(s)
        2. Add new Admin
        3. Add new User
        4. List of Users
        5. List of Bikes
        6. Load Data
        7. Exit
### details of Class(Bike):
    it should contain many properties and methods like: `IsRented` or `SerialNumber` and etc.
### details of Class(ElectricBike):
    it should contain many properties and methods like: `IsRented` or `SerialNumber` or `Charged` and 
    etc.
### details of Class(RoadBike):
    it should contain many properties and methods like: `IsRented` or `SerialNumber` and 
    etc.
### Class(User) details:
    it should completely implemented and contain `username`, `RentalList`, etc...

NOTE!
maximum 3 Bikes can rent every single person.
