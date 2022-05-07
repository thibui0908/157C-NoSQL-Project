from billing import *
from sympy import re
import pymongo
from datetime import *

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["rental"]
colUsers = mydb["users"]
colMovies = mydb["movies"]
colBilling = mydb["billing"]

class User:

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
        self.loggedIn = True


def home():
    print("-------------------------")
    print("Welcome to Movie Rental")
    print("Login, Register, Exit")
    print("-------------------------")
    a = input("What would you like to do: ")
    if(a == "Register" or a == "register"):
        register()
    elif(a == "Login" or a == "login"):
        login()
    elif(a == "Exit" or a == "exit"):
        exit()
    else:
        print("Choose a valid option")
        home('')

def register():
    name = input("Name: ")
    username = input("Username: ")
    password = input("Password: ")
    user = User(name, username, password)
    userDict = { "name": name, "username": username, "password" : password }
    x = colUsers.insert_one(userDict)
    # print(x.inserted_id)
    print("Successfully Registered, " + user.name)
    home()


def login():
    inputUsername     = input("Username: ")
    inputPassword     = input("Password: ")
    userDoc           = colUsers.find_one({"username" : inputUsername, "password" : inputPassword})
    retrievedName     = userDoc["name"]
    retrievedUsername = userDoc["username"]
    retrievedPassword = userDoc["password"]
    loggedInUser = User(retrievedName, retrievedUsername, retrievedPassword)
    if(inputPassword == retrievedPassword):
        print("Welcome, " + loggedInUser.name)
    else:
        print("Incorrect username or password")
        login()
    menu(loggedInUser)

#home menu
def menu(loggedInUser):
    print("####################")
    print("--------Menu--------")
    print("Account Settings===1")
    print("Logout=============2")

    #routes to billing
    print("Billing============3")
    print("Rent Film============4")
    print("Return Film============5")


    print("####################")
    menuOption = input("Enter number to choose option: ")
    if(menuOption == "1"):
        accountSetting(loggedInUser)
    elif(menuOption == "2"):
        exit()
    elif(menuOption == "3"):
        billingHome(loggedInUser)
    elif(menuOption == "4"):
        rentFilm()
    elif(menuOption == "5"):
        returnFilm()
    else:
        print("Choose a valid option")
        menu(loggedInUser)

def accountSetting(loggedInUser):
    print("####################")
    print("--Account Settings--")
    print("View Details=======1")
    print("Update Details=====2")
    print("Delete Account=====3")
    print("Logout=============4")
    print("####################")
    accountSettingOption = input("Enter number to choose option: ")
    if(accountSettingOption == "1"):
        viewAccountDetials(loggedInUser)
    elif(accountSettingOption == "2"):
        updateAccountDetials(loggedInUser)
    elif(accountSettingOption == "3"):
        deleteUser(loggedInUser)
    elif(accountSettingOption == "4"):
        exit()
    else:
        print("Choose a valid option")
        menu()


def viewAccountDetials(loggedInUser):
    print("--------------------")
    print("Name: "+loggedInUser.name)
    print("Username: "+loggedInUser.username)
    print("Password: "+loggedInUser.password)
    print("--------------------")
    menu(loggedInUser)

def updateAccountDetials(loggedInUser):
    print("####################")
    print("Update Name========1")
    print("Update Password====2")
    print("Logout=============3")
    print("####################")
    updateAccountOption = input("Enter number to choose option: ")
    if(updateAccountOption == "1"):
        updateName(loggedInUser)
    elif(updateAccountOption == "2"):
        updatePassword(loggedInUser)
    elif(updateAccountOption == "3"):
        exit()

def updateName(loggedInUser):
    print("--------------------")
    print("Current Name: "+loggedInUser.name)
    updatedName = input("Enter new name: ")
    userDoc = { "username": loggedInUser.username }
    newNameQuery = { "$set": { "name": updatedName } }
    colUsers.update_one(userDoc, newNameQuery)
    print("Name updated Successfully to "+updatedName)
    loggedInUser.name = updatedName
    menu(loggedInUser)


def updatePassword(loggedInUser):
    print("--------------------")
    print("Current Password: "+loggedInUser.password)
    updatedPassword = input("Enter new password: ")
    userDoc = { "username": loggedInUser.username }
    newPasswordQuery = { "$set": { "password": updatedPassword } }
    colUsers.update_one(userDoc, newPasswordQuery)
    print("Name updated Successfully to "+updatedPassword)
    loggedInUser.password = updatedPassword
    menu(loggedInUser)

def rentFilm(user_id):
    print("--------------------")
    filmTitle = input("Input film title: ")
    purchase_date = datetime.date.today()
    due_date = purchase_date + timedelta(days=10)
    #create billing 
    rentQuery = { "film_title": filmTitle, "purchase_date": purchase_date, "films_due_date": due_date}
    colBilling.insertOne(rentQuery)
    #add billing to user
    billing = colBilling.find(
        {"film_title": filmTitle, "purchase_date": str(purchase_date)})
    colUsers.update_one({"_id": user_id} , {"$push": {"transactions": billing}})    
    #decrease film copy
    colMovies.updateOne({"title": filmTitle},{"$inc": {"amount_copies": -1}})


def returnFilm():
    print("--------------------")
    #return film
    billingID = input("Input return billing ID: ")
    returnFilm = {"billing_id": billingID}
    returnDay = datetime.date.today()
    updateBilling = {"$set":{"films_return_date": returnDay}}
    returnQuery = { returnFilm, updateBilling}
    colBilling.updateOne(returnQuery)
    dueDay = colBilling.find(returnFilm, {"films_due_date" : 1})
    #check if there is a late fee
    if returnDay > dueDay:
        lateFee = returnDay - dueDay
        print("Late fee: $" + lateFee )

    #add increase number of copies
    returnFilmTitle = colBilling.find(returnFilm, {"films_title" : 1})
    colMovies.updateOne({"title": returnFilmTitle},{"$inc": {"amount_copies": 1}})



    

def deleteUser(loggedInUser):
    print("Deleting user will be permanent!")
    deleteFlag = input("If yes please, type \"delete\": ")
    if(deleteFlag == "delete"):
        userDoc = colUsers.find_one({"username" : loggedInUser.username})
        docID = userDoc["_id"]
        myquery = { "_id": docID}
        colUsers.delete_one(myquery)
    print("Account Successfully Deleted, "+loggedInUser.name)
    exit()


def exit():
    quit()

home()