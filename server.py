from flask import Flask, render_template, request, redirect, url_for
import time

import queries 
app = Flask(__name__)
database_conn = None

@app.route('/',methods = ['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        return "<h1>OK</h1>"

# @app.route('/boardGames',methods=['GET','POST'])
# def boardGames():
#     return "<h1>board games</h1>"

@app.route('/genre',methods=['GET','POST'])
def genre():
    
    if request.method == 'GET':
        return render_template('genre_page.html')


@app.route('/specifiedGenre/<id>', methods = ['GET','POST'])
def specifiedGenre(id):

    global database_conn

    if request.method == 'GET':
        myCollection = database_conn['LatestGames']

        # retVal = queries.get_game_names(id,myCollection)
        return render_template('Specified_genre_page.html',genre=id)

@app.route('/search', methods = ['POST'])
def search():
    global database_conn
    myCollection = database_conn['LatestGames']
    myQuery = queries.search_results(myCollection, request.form['search_val'])
    return render_template('searchResults.html',searchVal=request.form['search_val'],results = myQuery)



# @app.route('/loadthis')
# def loadthis():
#     return render_template('lazyLoader.html')

@app.route('/lazyload')
def lazy_load():
    time.sleep(0.2)  # Used to simulate delay
    global database_conn
    myCollection = database_conn['LatestGames']

    if request.args:
            myGenre = request.args.get("g")
            counter = int(request.args.get("c"))  # The 'counter' value sent in the QS
            res = queries.lazy_loading(myGenre, myCollection, counter, queries.get_game_count(myGenre, myCollection))            

    return res

@app.route('/displayData')
def display_game_data():
    print("Inside game data")
    global database_conn
    if request.args:
        print(request.args.get('name'))
    retVal,secVal = queries.display_game_data(database_conn, request.args.get('name'))
    # print(retVal)
    return render_template('game_description_page.html',data=retVal,sec=secVal)


if __name__ == '__main__':
    queries.hello()
    database_conn = queries.get_connection()
    app.run(debug=True)



# myString = "{{url_for('displayData',game_name='+document.getElementById(`game_name`))}}"
# "this.href='{{url_for(`displayData`,game_name='+document.getElementById(`game_name`).innerText+')}}'"