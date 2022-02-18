from pymongo import MongoClient
from flask import make_response,jsonify
import re   
def hello():
    print("Hello World")

def get_connection():
    # 'mongodb://Ninja:ninja123@gamehunt-shard-00-00.efvuz.mongodb.net:27017,gamehunt-shard-00-01.efvuz.mongodb.net:27017,gamehunt-shard-00-02.efvuz.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-p6woqh-shard-0&authSource=admin&retryWrites=true&w=majority'
    # mongodb+srv://Ninja:ninja123@gamehunt.efvuz.mongodb.net/dataDump?retryWrites=true&w=majority
    cluster = MongoClient('mongodb://Ninja:ninja123@gamehunt-shard-00-00.efvuz.mongodb.net:27017,gamehunt-shard-00-01.efvuz.mongodb.net:27017,gamehunt-shard-00-02.efvuz.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-p6woqh-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = cluster["dataDump"]
    return db

def get_game_count(genre,collection):
    my_query = collection.count_documents({"genres":genre})
    return my_query

def get_search_count(search_val,collection):
    my_query = collection.count_documents({"name":{"$regex":f'^.*{search_val}.*$'}})
    return my_query

def get_game_names(genre,collection):
    my_query = list(collection.find({"genres":genre},{"_id":0,"name":1,"Background_image":1},limit=15))
    print(my_query)
    return my_query

def lazy_loading(genre,collection,counter,total_entries):
    print("Value of genre",genre)
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
    else:
        # {"genres.0":{$exists:false}}
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

def search_results(collection, search_val):
    query = list(collection.find({"name":{"$regex":f'^.*{search_val}.*$'}},{"_id":0,"name":1,"Background_image":1}))
    return query



def display_game_data(collection,game_name):
    mainData = collection['LatestGames']
    secondaryData = collection['Download,Summary']

    mainData = list(mainData.find({"name":game_name}))

    secondData = list(secondaryData.find({"Name":game_name},{"_id":0,"SteamURL":1,"Graphics":1,"Storage":1,"Memory":1,"OriginalCost":1,"Languages":1,"Description":1,"Tags":1}))
    if len(secondData) == 0:
        return mainData[0],"Null"
    else:
        return mainData[0],secondData[0]