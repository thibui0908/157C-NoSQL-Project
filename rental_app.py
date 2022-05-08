from bson import ObjectId
from billing import *
import pymongo
from pprint import pprint
from datetime import datetime
from datetime import *


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["rental"]
colUsers = mydb["users"]
colMovies = mydb["movies"]
colBilling = mydb["billing"]

class User:

    def __init__(self, user_id, name, username, password):
        self.user_id = user_id
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
    user = User(user_id = 0, name= name, username=username, password=password)
    userDict = { "name": name, "username": username, "password" : password, "transactions": [] , "balance": 0 }
    x = colUsers.insert_one(userDict)
    user.user_id = x.inserted_id
    print("Successfully Registered, " + user.name)
    home()

def login():
    inputUsername     = input("Username: ")
    inputPassword     = input("Password: ")
    userDoc           = colUsers.find_one({"username" : inputUsername, "password" : inputPassword})
    retrievedId       = userDoc["_id"]
    retrievedName     = userDoc["name"]
    retrievedUsername = userDoc["username"]
    retrievedPassword = userDoc["password"]
    loggedInUser = User(retrievedId, retrievedName, retrievedUsername, retrievedPassword)
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

    #routes to billing
    print("Billing============2")

    # routes to search
    print("Browse=============3")

    #Rent Film
    print("Rent Film==========4")

    #Return Film
    print("Return Film========5")
    
    #Logout
    print("Logout=============6")

    print("####################")
    menuOption = input("Enter number to choose option: ")
    if(menuOption == "1"):
        accountSetting(loggedInUser)
    elif(menuOption == "6"):
        exit()
    elif(menuOption == "2"):
        billingHome(loggedInUser)
    elif (menuOption == "3"):
        browse_films(loggedInUser)
    elif (menuOption == "4"):
        rentFilm(loggedInUser)
    elif (menuOption == "5"):
        returnFilm(loggedInUser)
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
        menu(loggedInUser)


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
    print("Password updated Successfully to "+updatedPassword)
    loggedInUser.password = updatedPassword
    menu(loggedInUser)

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

# billing 


class Billing:

    def __init__(self, film_title, purchase_date, return_date):
        self.film_title = film_title
        self.purchase_date = purchase_date
        self.return_date = return_date

# to be called when checking out


def addBilling(user_id, film_title):
    purchase_date = datetime.now()
    return_date = datetime.now() + timedelta(days=10)

    newBilling = Billing(film_title, purchase_date.strftime(
        "%d-%m-%Y"), return_date.strftime("%d-%m-%Y"))

    billingDict = {"film_title": film_title, purchase_date: str(
        purchase_date), return_date: str(return_date)}

    #update user's transactions and insert to system's billing db
    colBilling.insert_one(billingDict)
    billing = colBilling.find(
        {"film_title": film_title, "purchase_date": str(purchase_date)})
    colUsers.update_one({"_id": user_id}, {"$push": {"transactions": billing}})

# system check for unreturned titles
# call this function to add a penalty


def addPenalty(user):
    colUsers.update_one({"_id": user.user_id}, {
                        "$inc": {"balance": float(10)}})


def billingHome(user):
    print("-------------------------")
    print("You're in the billing page")
    print("Check balance [CB], Make a payment[PM], Return to home [X]")
    print("-------------------------")
    a = input("What would you like to do: ")
    if(a == "CB" or a == "cb"):
        #check balance funct
        checkBalance(user)
    elif(a == "PM" or a == "pm"):
        #payment funct
        makePayment(user)
    elif(a == "X" or a == "x"):
        menu(user)
    else:
        print("Choose a valid option")
        billingHome(user)

# Only valid when user is logged in


def checkBalance(user):
    print("Your balance is: \n")
    result = colUsers.find_one({"_id": user.user_id}, {"_id": 0, "balance": 1})
    print(result["balance"], " dollars")

    billingHome(user)


def makePayment(user):
    amount = input("Enter the amount you want to pay: \n")
    
    amount = float(amount)

    colUsers.update_one({"_id": user.user_id}, {
                        "$inc": {"balance": amount * (-1)}})

    print("You successfully made a payment of ", amount, " dollars\n")
    checkBalance(user)

    billingHome(user)

def browse_films(loggedInUser):
    query_selection = input(
        "\nSELECT THE QUERY YOU WOULD LIKE TO RUN: \n\n[1] Search films based on title\n[2] Search films based on price\n[3] Search films based on their popularity\n"
        "[4] Search films based on year released\n[5] Search films based on movie runtime\n"
        "[6] Search films based on their ratings\n[7] Search films based on their language\n[h] Return to Home\n")
    my_query = {}
    while (query_selection != 'q'):
        if query_selection == '1':
            title_to_search = input("Type the movie title you would like to search: ")
            my_query = {"title": title_to_search}
        elif query_selection == '2':
            price = input("Type the maximum movie price you are looking for: ")
            my_query = {"price": {"$lte": float(price)}}
        elif query_selection == '3':
            popularity = input("Type the minimum movie popularity you would like to search: ")
            my_query = {"popularity": {"$gte": float(popularity)}}
        elif query_selection == '4':
            year_released = input("Type the release date you would like to search (YYYY): ")
            my_query = {"release_date": {"$gte": year_released + "-1-1"}}
        elif query_selection == '5':
            runtime = input("Type the maximum runtime (in minutes) you are looking for: ")
            my_query = {"runtime": {"$lte": float(runtime)}}
        elif query_selection == '6':
            ratings = input("Type the minimum movie rating you would like to search: ")
            my_query = {"voting_average": {"$gte": float(ratings)}}
        elif query_selection == '7':
            language = input("Type the movie language you would like to search: ")
            my_query = {"original_language": language}
        elif query_selection == 'h':
            menu(loggedInUser)
        else:
            print("Choose a valid option")
            browse_films(loggedInUser)

        # limit the docs to 10 and remove id
        mydoc = colMovies.find(my_query, {"_id": 0}).limit(10)

        for x in mydoc:
            pprint(x)
            print("\n")

        # check out


        query_selection = input(
            "\nSELECT THE QUERY YOU WOULD LIKE TO RUN: \n\n[1] Search films based on title\n[2] Search films based on price\n[3] Search films based on their popularity\n"
            "[4] Search films based on year released\n[5] Search films based on movie runtime\n"
            "[6] Search films based on their ratings\n[7] Search films based on their language\n[h] Return to Home\n")

def rentFilm(loggedInUser):
    print("--------------------")
    filmTitle = input("Input film title: ")
    purchase_date = datetime.now().date()
    due_date = purchase_date + timedelta(days=10)
    # print(type(purchase_date))
    # print(type(due_date))
    numCopy = colMovies.find_one({"title": filmTitle}, {"_id":0,"amount_copies": 1})
    # print(numCopy["amount_copies"])
    if numCopy["amount_copies"]<=0:
        print("This movie is not avaible to rent. No copies left!")
        menu(loggedInUser)
    else :
        #create billing 
        rentQuery = { "film_title": filmTitle, "purchase_date": purchase_date.isoformat(), "films_due_date": due_date.isoformat()}
        colDocument = colBilling.insert_one(rentQuery)
        # print(colDocument.inserted_id)
        # Add billing to user
        colUsers.update_one({"username": loggedInUser.username} , {"$push": {"transactions": colDocument.inserted_id}})
        userDocument = colUsers.find_one({"username": loggedInUser.username})
        # print(userDocument["transactions"])
        # print("Balance before: "+str(userDocument["balance"]))
        newBalance = userDocument["balance"] + 5
        colUsers.update_one({"username": loggedInUser.username} , {"$set": {"balance": newBalance}})
        #decrease film copy
        colMovies.update_one({"title": filmTitle},{"$inc": {"amount_copies": -1}})
        print("--------------------")
        print("New Balance: "+str(newBalance))
        billingRecipt = colBilling.find_one({"_id":colDocument.inserted_id})
        print("Recipt:")
        billingRecipt["billing_id"] = billingRecipt["_id"]
        del billingRecipt["_id"]
        billingRecipt["billing_id"] = str(billingRecipt["billing_id"])
        pprint(billingRecipt)
        print("Billing ID will be requried for returning film!")
        menu(loggedInUser)


def returnFilm(loggedInUser):
    print("--------------------")
    # Return film
    billingID = input("Input return billing ID: ")
    returnFilmID = {"_id": ObjectId(billingID)} 
    returnDate = datetime.now().date().isoformat()
    # testDate = datetime(2022, 5, 27).date().isoformat()
    # print(testDate)
    updateBilling = {"$set":{"films_return_date": returnDate}}
    #print(returnDate)
    colBilling.update_one( returnFilmID , updateBilling )
    dueDate = colBilling.find_one(returnFilmID, {"films_due_date" : 1})
    #check if there is a late fee
    #print(dueDate["films_due_date"])
    if returnDate > dueDate["films_due_date"]:
        lateFee = abs(datetime.strptime(returnDate, "%Y-%m-%d").date() - datetime.strptime(dueDate["films_due_date"], "%Y-%m-%d").date()).days
        print("Late fee: $" + str(lateFee) )
        colUsers.update_one({"username" : loggedInUser.username},{"$inc" : {"balance" : lateFee}})
        userBalance = colUsers.find_one({"username" : loggedInUser.username}, {"balance":1})
        print("New Balance: "+str(userBalance["balance"]))
    # Add increase number of copies
    returnFilmTitle = colBilling.find_one(returnFilmID, {"film_title" : 1})
    colMovies.update_one({"title": returnFilmTitle["film_title"]},{"$inc": {"amount_copies": 1}})
    print("Movie returned! Return date: "+str(returnDate))
    menu(loggedInUser)

home()