import pymongo
from pprint import pprint
import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["rental"]
mycol = mydb["movies"]

query_selection = input("\nSELECT THE QUERY YOU WOULD LIKE TO RUN: \n\n[1] Search films based on title\n[2] Search films based on price\n[3] Search films based on their popularity\n"
                        "[4] Search films based on year released\n[5] Search films based on movie runtime\n"
                        "[6] Search films based on their ratings\n[7] Search films based on their language\n[q] Quit\n")
my_query = {}
while(query_selection!='q'):
    if query_selection == '1':
        title_to_search = input("Type the movie title you would like to search: ")
        my_query = {"title": title_to_search}
    if query_selection == '2':
        price = input("Type the maximum movie price you are looking for: ")
        my_query = {"price": {"$lte": float(price)}}
    if query_selection == '3':
        popularity = input("Type the minimum movie popularity you would like to search: ")
        my_query = {"popularity": {"$gte": float(popularity)}}
    if query_selection == '4':
        year_released = input("Type the release date you would like to search (YYYY): ")
        my_query = {"release_date": {"gte": datetime.datetime(year_released,1,1)}}
    if query_selection == '5':
        runtime = input("Type the maximum runtime (in minutes) you are looking for: ")
        my_query = {"runtime": {"$lte": float(runtime)}}
    if query_selection == '6':
        ratings = input("Type the minimum movie rating you would like to search: ")
        my_query = {"voting_average": {"$gte": float(ratings)}}
    if query_selection == '7':
        language = input("Type the movie language you would like to search: ")
        my_query = {"original_language": language}

    # limit the docs to 10 and remove id
    mydoc = mycol.find(my_query, {"_id": 0}).limit(10)

    for x in mydoc:
        pprint(x)
        print("\n")

    # option to rent

    query_selection = input(
        "\nSELECT THE QUERY YOU WOULD LIKE TO RUN: \n\n[1] Search films based on title\n[2] Search films based on price\n[3] Search films based on their popularity\n"
        "[4] Search films based on year released\n[5] Search films based on movie runtime\n"
        "[6] Search films based on their ratings\n[7] Search films based on their language\n[q] Quit\n")