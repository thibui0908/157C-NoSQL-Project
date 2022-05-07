from billing import *
import pymongo

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
    user = User(name, username, password)
    userDict = { "name": name, "username": username, "password" : password }
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
    print("Logout=============2")

    #routes to billing
    print("Billing============3")

    print("####################")
    menuOption = input("Enter number to choose option: ")
    if(menuOption == "1"):
        accountSetting(loggedInUser)
    elif(menuOption == "2"):
        exit()
    elif(menuOption == "3"):
        billingHome(loggedInUser)
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