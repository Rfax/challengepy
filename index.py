from db_connection import *

from flask import Flask, request, session, redirect, url_for, abort
from user_class import *
from club_class import *
from scraper import * # Web Scraping utility functions for Online Clubs with Penn.
import json

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'ne%qp*x^@fwca?ye'

#initializes the database
def init_db():
    reset_db()
    add_clubs_to_db (scrape_penn_clubs())
    User.create_user('jen','Jennifer', '12345')
    print("Database Initialized")
    

@app.route('/')
def main():
    return "Welcome to Penn Club Review!"

@app.route('/api')
def api():
    text = "Welcome to the Penn Club Review API! Here are the available functions:"
    text += "\n /api/clubs"
    text += "\n /api/clubs/search/name/<text>"
    text += "\n /api/clubs/search/tag/<text>"
    text += "\n /api/init"
    text += "\n /api/user/login"
    text += "\n /api/user/logout"
    text += "\n /api/user/<username>"
    text += "\n /api/favorite/add/<club_id>"
    text += "\n /api/favorite/remove/<club_id>"
    text += "\n /api/favorite/"
    text += "\n /api/favorite/rank"
    text += "\n /api/favorite/rankall"
    text += "\n "

    
    return text
    
@app.route('/api/clubs', methods=['GET', 'POST'])
def api_clubs():
    User.check_login()
    if request.method == 'POST':
        if request.get_json():
            data = request.get_json()
            
            if ('name' in data) and ('description' in data):
                
                if ('tags' in data):
                    tags = data['tags']
                else:
                    tags = []
                    
                c = Club.create_club (data['name'],data['description'], tags)
                
                result = "Club successfully created, with attributes: " + str(json.dumps(c.__dict__))
                
            else:
                
                result = "Error: JSON not valid"

        else:
            result = "Error: No JSON recieved..." 
    else:
        
        where = ""
        params = ()
        filter = False
        
        id = request.args.get('id', '')
        name = request.args.get('name', '')
        desc = request.args.get('desc', '')

        print("id: " + id + ", type: " + str(type(id)))
        print("name: " + name + ", type: " + str(type(name)))
        print("desc: " + desc + ", type: " + str(type(desc)))
        
        if (id) != "":
            if filter:
                where += " AND "
            else:
                where += " WHERE "
            
            filter = True
            where += "id = %s"
            params = params + (id,)
        
        if (name) != "":
            if filter:
                where += " AND "
            else:
                where += " WHERE "
            
            filter = True
            where += "name = %s" 
            params = params + (name,)
            
        if (desc) != "":
            if filter:
                where += " AND "
            else:
                where += " WHERE "
            
            filter = True
            where += "description = %s" 
            params = params + (desc,)
            
        print ("Where: " + where)
        print ("Params: " + str(params))
                
        result = Club.str_convert(Club.get_all_clubs(where, params))
        
        
    return str(result)

@app.route('/api/clubs/search/name/<text>')
def api_club_name_search(text):
    User.check_login()
    return Club.str_convert(Club.search_clubs_by_name(text))
    

@app.route('/api/clubs/search/tag/<text>')
def api_club_tag_search(text):
    User.check_login()        
    return Club.str_convert(Club.search_clubs_by_tag(text))

@app.route('/api/init')
def api_init_db():
    init_db()
    return "Database initialized successfully"

@app.route('/api/user/login', methods=['GET', 'POST'])
def api_login():
    
    if request.method == 'POST':
        if request.get_json():
            data = request.get_json()
            
            if ('username' not in data)  or ('password' not in data):
                return "Please send username and password"
            
            u = User.read_user_by_username(data['username'])
            
            if(u == None):
                return "User/Password combination is invalid"

            
            return u.login(data['password'])
                            
        else:
            return "Error: No JSON recieved..."
            
    else:
        return "Please login by sending a json with POST"
    
@app.route('/api/user/logout')
def api_logout():
    User.logout()
    return "Logout Successful"

@app.route('/api/user/<username>')
def api_show_user(username):
    User.check_login()
    u = User.read_user_by_username(username)
    if u == None:
        return 'No user found...'
    return str([u.username, u.name])


@app.route('/api/favorite/add/<club_id>')
def api_add_favorite(club_id):
    User.check_login()
    u = User.get_current_user()    
    return u.add_favorite_club(club_id)

@app.route('/api/favorite/remove/<club_id>')
def api_remove_favorite(club_id):
    User.check_login()
    u = User.get_current_user()    
    return u.remove_favorite_club(club_id)

@app.route('/api/favorite/')
def api_view_favorite():
    User.check_login()
    u = User.get_current_user()
    
    clubs = []
    
    for club in u.favorite_clubs: 
        clubs.append(club.__dict__)
            
    return str(clubs)

@app.route('/api/favorite/rank')
def api_favorite_rank():
    return str(Club.favorite_ranking())

@app.route('/api/favorite/rankall')
def api_favorite_rankall():
    return str(Club.favorite_ranking(True))

if __name__ == '__main__':
    app.run()
