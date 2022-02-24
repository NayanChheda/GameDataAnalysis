from flask import Flask, render_template, request, redirect, url_for
import time
import queries 

app = Flask(__name__)
database_conn = None

# Home page
@app.route('/')
def index():
        return render_template('index.html')

# Genre page
@app.route('/genre')
def genre():

        return render_template('genre_page.html')


# Specified Genre Page
@app.route('/specifiedGenre/<id>')
def specifiedGenre(id):

        return render_template('Specified_genre_page.html',genre=id)

# Search results
@app.route('/search', methods = ['POST'])
def search():

    global database_conn
    myCollection = database_conn['LatestGames']
    myQuery = queries.search_results(myCollection, request.form['search_val'])
    return render_template('searchResults.html',searchVal=request.form['search_val'],results = myQuery)



# Lazy loading
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

# Display game data
@app.route('/displayData')
def display_game_data():
    global database_conn
    if request.args:
        retVal,secVal = queries.display_game_data(database_conn, request.args.get('name'))
    return render_template('game_description_page.html',data=retVal,sec=secVal)


# Main function
if __name__ == '__main__':
    queries.hello()
    database_conn = queries.get_connection()
    app.run(debug=True)
