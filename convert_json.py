import csv
import json
import datetime
from tokenize import Double
 
# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):
     
    # create a dictionary
    data = []
     
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
             
            # Assuming a column named 'No' to
            # be the primary key
            # key = rows['id']
            #price
            price = int (rows["price"])
            rows["price"] = price
            
            #runtime
            runtime = int (rows["runtime"])
            rows["runtime"] = runtime

            #popularity
            popularity = float (rows["popularity"])
            rows["popularity"] = popularity
            
            #vote_average
            vote_average = float (rows["vote_average"])
            rows["vote_average"] = vote_average

            #amount_copies
            amount_copies = int (rows["amount_copies"])
            rows["amount_copies"] = amount_copies

            #vote_count
            vote_count = int (rows["vote_count"])
            rows["vote_count"] = vote_count

            #date_released
            year_released = datetime.strptime(rows["release_date"], '%d/%m/%y')
            rows["release_date"] = year_released

            data.append(rows)
 
    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
         
# Driver Code
 
# Decide the two file paths according to your
# computer system
csvFilePath = r'/Users/ajakasan/Desktop/My Stuff/Class/CS 157C/Project/movies_metadata.csv'
jsonFilePath = r'/Users/ajakasan/Desktop/My Stuff/Class/CS 157C/Project/test.json'
 
# Call the make_json function
make_json(csvFilePath, jsonFilePath)