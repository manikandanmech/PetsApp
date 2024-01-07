import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="santhi12",
    database="petshopapp")

from datetime import date

mycursor = mydb.cursor()


def user_login(username):
    mycursor.execute("select * from user_details where user_name like %s",(username,))
    data = mycursor.fetchall()
    name = data[0][1]
    if name == username:
        return 1


def order(user_name):
    pet_lists="""
    -------------------------------------------------
    |       pets lists     color       Age          |
    |        1.cat        black         5           |
    |        2.dog        white         10          |
    |        3.hen        green         8           |
    -------------------------------------------------
        """
    print(pet_lists)

    d = {1: "cat", 2: "dog",3:"hen"}
    print("Enter your pet lists option :")
    choice = int(input())
    if choice >= 1 and choice <= 3:
        pets = d[choice]
        mycursor.execute("select pet_cost from pets_details where pet_name like (%s)",(pets,))
        data = mycursor.fetchone()
        pet_cost = int(data[0])
        print("Enter your count of order :")
        count = int(input())
        global totalcost
        totalcost = pet_cost * count
        Date=date.today()
        mycursor.execute("insert into petsorder_details(user_name,pet_name,pet_totalcost,Date) values (%s,%s,%s,%s)",
                         (user_name,pets,totalcost,Date,))
        mydb.commit()
        mycursor.execute("select * from petsorder_details where user_name like %s", (user_name,))
        data = mycursor.fetchall()
        name = data[-1][0]
        pets = data[-1][1]
        pet_cost = data[-1][2]
        Date = data[-1][3]
        print("Ordered date: %s" % Date)
        print("Name of oder person %s" % name)
        print("Ordered pet is %s" % pets)
        print("Total Cost of %s" + pets +" is %s" % pet_cost)
        return 1
    else:
        print("Pet is not available.chose correct option")
        return 0

def display(username):
    mycursor.execute("select * from petsorder_details where user_name like %s", (username,))
    data = mycursor.fetchall()
    if data:
        print("Name of the user :%s" % data[0][0])
        for row in range(len(data)):
            print("pets Ordered :%s" % data[row][1])
            print("Total Cost of pets :%s" % data[row][2])
            print("Ordered Date :%s" % data[row][3])
    else:
        print("No Records found!")
    return 1

print("---------------welcome to PetsApp----------------")
destination = input("Are you a user or newuser?" + '\n' +
                    " Type your destination :")
destination = destination.lower()

if destination == "newuser":
    user_name = input("Enter your name :")
    moblie_no = input("Enter your Phone number :")
    Address = input("Enter your address :")
    mycursor.execute("insert into user_details(user_id,user_name,mobile_no,Address) values(NULL,%s,%s,%s)",
                     (user_name,moblie_no,Address,))
    mydb.commit()
    print("Registration success !!" 
          "Welcome to PetsApp")

if destination == "user":
    username = input("Enter your name :")
    if user_login(username):
        print("1:Order your pets")
        print("2:view your previous order lists")
        choice = int(input("Enter your option :"))
        if choice == 1:
            if order(username):
                print("your Order is Success")
        elif choice == 2:
            display(username)
        else:
            print("Invalid your choice")
    else:
        print("User does not exist")
