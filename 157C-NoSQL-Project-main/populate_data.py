import pymongo
import json

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["rental"]
mycol = mydb["movies"]

with open('/Users/ajakasan/Desktop/My Stuff/Class/CS 157C/Project/test.json') as json_file:
    data = json.load(json_file)

# mylist = [
#   { "name": "Amy", "address": "Apple st 652"},
#   { "name": "Hannah", "address": "Mountain 21"},
#   { "name": "Michael", "address": "Valley 345"},
#   { "name": "Sandy", "address": "Ocean blvd 2"},
#   { "name": "Betty", "address": "Green Grass 1"},
#   { "name": "Richard", "address": "Sky st 331"},
#   { "name": "Susan", "address": "One way 98"},
#   { "name": "Vicky", "address": "Yellow Garden 2"},
#   { "name": "Ben", "address": "Park Lane 38"},
#   { "name": "William", "address": "Central st 954"},
#   { "name": "Chuck", "address": "Main Road 989"},
#   { "name": "Viola", "address": "Sideway 1633"}
# ]

print(data)

x = mycol.insert_many(data)

#print list of the _id values of the inserted documents:
print(x.inserted_ids)