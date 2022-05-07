import pymongo
from rental_application import *
from datetime import datetime
from datetime import timedelta

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["rental"]
colUsers = mydb["users"]
colMovies = mydb["movies"]
colBilling = mydb["billing"]


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
    
    billingDict = {"film_title" : film_title, purchase_date: str(purchase_date), return_date: str(return_date)}

    #update user's transactions and insert to system's billing db
    billing = colBilling.insert_one(billingDict)
    colUsers.update_one({user_id: user_id} , {"$push": {"transactions": billing}})

# system check for unreturned titles
# call this function to add a penalty

def addPenalty(user_id):
    colUsers.update_one({user_id: user_id}, {
                        "$inc": {"balance": float(10)}})

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

# Only valid when user is logged in

def checkBalance(user_id):
    print("Your balance is: \n")
    result = colUsers.find_one({user_id: user_id}, { "_id": 0, "balance": 1 })
    print(result, " dollars")

    billingHome()

def makePayment(user_id):
    amount = input("Enter the amount you want to pay: \n")

    colUsers.update_one({user_id: user_id}, {"$inc": {"balance": float(amount) } } )

    print("You successfully made a payment of ", amount, " dollars")

    billingHome()


