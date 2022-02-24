from pymongo import MongoClient
from flask import make_response,jsonify
import re   

# Testing function
def hello():
    print("Hello World")

# Get cluster connection
def get_connection():
    cluster = MongoClient('mongodb://Ninja:ninja123@gamehunt-shard-00-00.efvuz.mongodb.net:27017,gamehunt-shard-00-01.efvuz.mongodb.net:27017,gamehunt-shard-00-02.efvuz.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-p6woqh-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = cluster["dataDump"]
    return db

# Get total entries of a genre
def get_game_count(genre,collection):
    my_query = collection.count_documents({"genres":genre})
    return my_query

# Get search count
def get_search_count(search_val,collection):
    my_query = collection.count_documents({"name":{"$regex":f'^.*{search_val}.*$'}})
    return my_query

# Get game names of a specific genre
def get_game_names(genre,collection):
    my_query = list(collection.find({"genres":genre},{"_id":0,"name":1,"Background_image":1},limit=15))
    return my_query

# Lazy loading 
def lazy_loading(genre,collection,counter,total_entries):
    # If user selects a specific genre
    if genre != "Other":
        if counter == 0:
            query = list(collection.find({"genres":genre},{"_id":0,"name":1,"Background_image":1},limit=15).sort("ratings_count",-1))
            print(type(query))
            res = make_response(jsonify(query),200)

        elif counter == total_entries:
            res = make_response(jsonify({}),200)

        else:
            query = list(collection.find({"genres":genre},{"_id":0,"name":1,"Background_image":1},limit=15,skip=(counter+15)).sort("ratings_count",-1))
            res = make_response(jsonify(query),200)
    # If user selects other genre
    else:
        if counter == 0:
            query = list(collection.find({"genres.0":{"$exists":False}},{"_id":0,"name":1,"Background_image":1},limit=15).sort("ratings_count",-1))
            print(type(query))
            res = make_response(jsonify(query),200)

        elif counter == total_entries:
            res = make_response(jsonify({}),200)

        else:
            query = list(collection.find({"genres.0":{"$exists":False}},{"_id":0,"name":1,"Background_image":1},limit=15,skip=(counter+15)).sort("ratings_count",-1))
            res = make_response(jsonify(query),200)
    
    return res

# Fetch search results
def search_results(collection, search_val):
    query = list(collection.find({"name":{"$regex":f'^.*{search_val}.*$'}},{"_id":0,"name":1,"Background_image":1}))
    return query


# Display game data
def display_game_data(collection,game_name):
    mainData = collection['LatestGames']    # primary data
    secondaryData = collection['Download,Summary']  # secondary data

    mainData = list(mainData.find({"name":game_name}))
    secondData = list(secondaryData.find({"Name":game_name},{"_id":0,"SteamURL":1,"Graphics":1,"Storage":1,"Memory":1,"OriginalCost":1,"Languages":1,"Description":1,"Tags":1}))

    # Return values according to availability of secondary data
    if len(secondData) == 0:
        return mainData[0],"Null"
    else:
        return mainData[0],secondData[0]