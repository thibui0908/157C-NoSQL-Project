import pymongo
from pprint import pprint

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["rental"]
mycol = mydb["movies"]

query_selection = input("\nSELECT THE QUERY YOU WOULD LIKE TO RUN: \n\n[1] Search a film using the title\n[2] Browse films based on price\n[3] Browse films based on their popularity\n[4] Search films based on year released\n[5] Search films based on movie runtime\n[q] Quit\n")
while(query_selection!='q'):
    if query_selection == '1':
        title_to_search = input("Type the movie title you would like to search: ")
        myquery1 = { "title": title_to_search }
    if query_selection == '2':
        price = input("Type the maximum movie price you are looking for: ")
        myquery = { "price": { "$lte": float(price) } }
    if query_selection == '3':
        popularity = input("Type the minimum movie popularity you would like to search: ")
        myquery = { "popularity": { "$gte": float(popularity) } }
    if query_selection == '4':
        year_released = input("Type the release date you would like to search (MM/DD/YY): ")
        myquery = { "release_date": year_released }
    if query_selection == '5':
        runtime = input("Type the maximum runtime (in minutes) you are looking for: ")
        myquery = { "runtime": { "$lte": float(runtime) } }

    mydoc = mycol.find(myquery)
    for x in mydoc:
        pprint(x)
    query_selection = input(
        "\nSELECT THE QUERY YOU WOULD LIKE TO RUN: \n\n[1] Search a film using the title\n[2] Browse films based on price\n[3] Browse films based on their popularity\n[4] Search films based on year released\n[q] Quit\n")

# mydoc = mycol.find(myquery)
#
# for x in mydoc:
#   pprint(x)