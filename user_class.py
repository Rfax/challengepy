import bcrypt
from flask import session, redirect, url_for, abort
from db_connection import *
from club_class import *

max_favorite_clubs = 1

class User:
  
    def __init__(self, id, username, name):
        self.id = id
        self.username = username
        self.name = name
        self.favorite_clubs = []
        
        
    #static method to create a user and add it to the databse
    @staticmethod
    def create_user (username, name, pwd):
        
        bpwd = bytes(pwd, encoding='utf-8')
        
        salt = bcrypt.gensalt() 
        hashed = bcrypt.hashpw(bpwd, salt) 
      
        query = "INSERT INTO pc_users (username, name, pwd) values (%s, %s, %s)"
        params = (username, name, hashed)
        
        dbcursor.execute (query, params)
        
        mydb.commit()
        
        id = dbcursor.lastrowid
        
        c = User(id, username, name)
            
        return c
    
    @staticmethod
    def logout ():

        session.pop('user_id', None)
        
        return 'Logout Successful'
            
    def login (self, pwd):
        
        if session.get('user_id') == self.id:
            return "User already logged in!"
        
        if(self.check_pwd(pwd)):
           
            session['user_id'] = self.id
            
            return 'Login Successful'
        else: 
            return "User/Password combination is invalid"
        
    def check_pwd (self, pwd):
        
        bpwd = bytes(pwd, encoding='utf-8')
        
        salt = bcrypt.gensalt() 
        hashed_input = bcrypt.hashpw(bpwd, salt)
        
        query = "SELECT pwd FROM pc_users WHERE id = %s;"
        
        params = (self.id,)
        
        dbcursor.execute (query, params)
        
        result = dbcursor.fetchone()
        
        #if no rows return, there is an error, and returning False is safer.
        if (result != None):
            hash = bytes(result[0], encoding='utf-8')
        else:
            return  False

        if bcrypt.checkpw(bpwd, hash): 
            return True
        else:
            return False
        
    @staticmethod
    def check_login():
        if User.get_current_user() == None:
            #return redirect(url_for('api_login'))
            abort (405)
    
    @staticmethod
    def read_user_by_username (username):
        query = "SELECT id, username, name FROM pc_users WHERE username = %s;"
                
        params = (username,)
        
        dbcursor.execute (query, params)
        
        result = dbcursor.fetchall()
                
        if (len(result) == 0):
            # no user found
            return None;
        
        
        # fills the Club object
        u =  User.fill_object(result[0])
        
        return u
    
    @staticmethod    
    def read_user(id):        
        query = "SELECT id, username, name FROM pc_users WHERE id = %s;"
                
        params = (id,)
                
        dbcursor.execute (query, params)
        
        result = dbcursor.fetchall()
                
        if (len(result) == 0):
            # no user found
            return None;
        
        
        # fills the Club object
        u =  User.fill_object(result[0])
        
        return u
    
    @staticmethod
    def fill_object(result):
        u = User(result[0], result[1], result[2])
        
        u.get_favorite_clubs()
                
        return u
    
    def get_favorite_clubs(self):
        query = "SELECT c.id FROM pc_user_favorites uf INNER JOIN pc_clubs c ON uf.club_id = c.id WHERE uf.user_id = %s;"
        
        params = (self.id,)
        
        dbcursor.execute (query, params)
                
        result = dbcursor.fetchall()
        
        
        for club in result:
            self.favorite_clubs.append((Club.read_club(club[0])))
            
    def add_favorite_club (self, club_id):
        
        club_id = int(club_id)     
              
        #check if club is already favorite
        for club in self.favorite_clubs:
            if club.id == club_id:
                return "Club is already in your favorites!"
                
        query = "INSERT INTO pc_user_favorites (club_id, user_id) values (%s, %s)"
        
        params = (club_id, self.id)
                        
        dbcursor.execute (query, params)
            
        mydb.commit()
        
        club = (Club.read_club(club_id))
        
        self.favorite_clubs.append(club)
        
        return "Club added: " + str(club.__dict__)
    
    def remove_favorite_club (self, club_id):
        
        x=0
        club_id = int(club_id)     
        
        #check if club is in favorite
        for club in self.favorite_clubs:
                        
            if (club.id == club_id):
                query = "DELETE FROM pc_user_favorites WHERE club_id = %s AND user_id = %s;"
                
                params = (club_id, self.id)
                        
                dbcursor.execute (query, params)
                    
                mydb.commit()
                                
                self.favorite_clubs.pop(x)
                
                
                return "Club removed: " + str(club.__dict__)
            
            x += 1
        
        return "Club was not in your favorites"
                                                 
                
        
        
    @staticmethod
    def get_current_user():
        return User.read_user(session.get('user_id'))

        
        
    
    

