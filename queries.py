from pymongo import MongoClient
from flask import make_response,jsonify
import re   
def hello():
    print("Hello World")

def get_connection():
    cluster = MongoClient('mongodb+srv://Ninja:ninja123@gamehunt.efvuz.mongodb.net/dataDump?retryWrites=true&w=majority')
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

    if counter == 0:
        query = list(collection.find({"genres":genre},{"_id":0,"name":1,"Background_image":1},limit=15))
        print(type(query))
        res = make_response(jsonify(query),200)

    elif counter == total_entries:
        res = make_response(jsonify({}),200)

    else:
        query = list(collection.find({"genres":genre},{"_id":0},limit=15,skip=(counter+15)))
        res = make_response(jsonify(query),200)
    
    return res

def search_results(collection, search_val,counter,total_entries):
    print("Inside search_results")
    print(counter,total_entries)

    if counter == 0:
        query = list(collection.find({"name":{"$regex":f'^.*{search_val}.*$'}},{"_id":0,"name":1,"Background_image":1},limit=15))
        print("Query Response")
        print(query)
        res = make_response(jsonify(query),200)
    elif counter == total_entries:
        res = make_response(jsonify({}),200)
    else:
        query = list(collection.find({"name":{"$regex":f'^.*{search_val}.*$'}},{"_id":0,"name":1,"Background_image":1},limit=15))
        print(query)
        res = make_response(jsonify(query),200)

    
    return res