import pymongo
from rental_application import *

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["rental"]
colUsers = mydb["users"]
colMovies = mydb["movies"]
colBilling = mydb["billing"]


class Billing:

    def __init__(self, film_title, purchase_date, password):
        self.film_title = film_title
        self.purchase_date = purchase_date
        self.password = password
        self.loggedIn = True

def billingHome():
    print("-------------------------")
    print("You're in the billing page")
    print("Check balance [CB], Make a payment[PM], Return to home [X]")
    print("-------------------------")
    a = input("What would you like to do: ")
    if(a == "CB" or a == "cb"):
        #check balance funct
        checkBalance()
    elif(a == "PM" or a == "pm"):
        #payment funct
        makePayment()
    elif(a == "X" or a == "x"):
        home('')
    else:
        print("Choose a valid option")

def checkBalance():
    print("Your balance is: ")
    billingHome()

def makePayment():
    print("Enter the amount you want to pay: ")
    billingHome()


