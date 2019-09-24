from db_connection import *
import json

class Club:
  
    #initializes values
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
        self.tags = []
        self.favorite_count = 0
  
    #static method to create a club and add it to the databse
    @staticmethod
    def create_club (name, description, tags = []):
      
        query = "INSERT INTO pc_clubs (name, description) values (%s, %s)"
        params = (name, description)
        
        dbcursor.execute (query, params)
        
        mydb.commit()
        
        id = dbcursor.lastrowid
        
        c = Club(id, name, description)
        
        for tag in tags:
            c.add_tag(tag)
            
        return c
    
    
    #adds the tag to the database and the python object
    def add_tag (self, tag):
      
        #check if tag exists
        query = "SELECT id, tag FROM pc_tags WHERE tag = %s"
        
        params = (str(tag),)
                
        dbcursor.execute (query, params)
        
        result = dbcursor.fetchall()
                
        #if tag does not exist, it needs to be created
        if (len(result) == 0):
            query = "INSERT INTO pc_tags (tag) values (%s)"
            
            params = (tag,)
            
            dbcursor.execute (query, params)
            
            mydb.commit()
            
            tag_id = dbcursor.lastrowid
            
        else:
            tag_id = result[0][0]
        
        
        #create tag association    
        query = "INSERT INTO pc_club_tags (club_id, tag_id) values (%s, %s)"
        
        params = (self.id, tag_id)
                
        dbcursor.execute (query, params)
            
        mydb.commit()
        
        self.tags.append(tag)
    
    #reads club through id and returns object 
    @staticmethod
    def read_club (id):        
        query = "SELECT id, name, description FROM pc_clubs WHERE id = %s;"
                
        params = (id,)
        
        dbcursor.execute (query, params)
        
        result = dbcursor.fetchall()
                
        if (len(result) == 0):
            # no club found
            return None;
        
        
        # fills the Club object
        c =  Club.fill_object(result[0])
        
        return c
    
    #fills the club object
    @staticmethod
    def fill_object(result):
        c = Club(result[0], result[1], result[2])
        
        c.get_tags()
        c.calc_favorites()
        
        return c
    
    #adds the tags to the club object
    def get_tags(self):
        query = "SELECT t.tag tag FROM pc_club_tags ct INNER JOIN pc_tags t ON ct.tag_id = t.id WHERE ct.club_id = %s;"
        
        params = (self.id,)
        
        dbcursor.execute (query, params)
        
        result = dbcursor.fetchall()
        
        for tag in result:
            self.tags.append(tag[0])
    
    #returns all the clubs given by a query with a filter
    @staticmethod        
    def get_all_clubs(where = "", params = ()):
        
        query = "SELECT id, name, description FROM pc_clubs" + where
                
        dbcursor.execute (query, params)
        
        result = dbcursor.fetchall()
                
        if (len(result) == 0):
            # no club found
            return None;
        
        clubs = []
                
        # fills all Club objects
        for club in result:
            clubs.append(Club.fill_object(club))
        
        return clubs
    
    #searches for clubs by their names
    @staticmethod
    def search_clubs_by_name(text):
        
        query = "SELECT id, name, description FROM pc_clubs WHERE name like %s"
        
        #adds wildcards to spaces so search is more complete
        text = text.replace(" ", "%")
                
        params = ('%' + text + '%',)
        
        dbcursor.execute (query, params)
        
        result = dbcursor.fetchall()
                
        if (len(result) == 0):
            # no club found
            return None;
        
        clubs = []
                
        # fills all Club objects
        for club in result:
            clubs.append(Club.fill_object(club))
        
        return clubs
    
    #searches for clubs by their tags
    @staticmethod
    def search_clubs_by_tag(text):
        
        #DISTINCT is used to make sure that a club won't appear twice even if it's two or more of it's tags appear in the search
        query = "SELECT DISTINCT c.id, c.name, c.description FROM pc_club_tags ct INNER JOIN pc_clubs c ON c.id = ct.club_id INNER JOIN pc_tags t on t.id = ct.tag_id WHERE t.tag like %s"
        
        #adds wildcards to spaces so search is more complete
        text = text.replace(" ", "%")
                
        params = ('%' + text + '%',)
        
        dbcursor.execute (query, params)
        
        result = dbcursor.fetchall()
                
        if (len(result) == 0):
            # no club found
            return None;
        
        clubs = []
                
        # fills all Club objects
        for club in result:
            clubs.append(Club.fill_object(club))
        
        return clubs
    
    #calculates how many users favorited the club
    def calc_favorites(self):
        
        query = "SELECT club_id, COUNT(*) qty FROM pc_user_favorites WHERE club_id = %s GROUP BY club_id;"
        
        params = (self.id,)
        
        dbcursor.execute (query, params)
        
        result = dbcursor.fetchone()
        
        #if no rows return, it means that it has not been favorited by anybody -> default value is 0
        if (result != None):
            self.favorite_count = result[1]
            
    #returns all the clubs, ranked by popularity
    @staticmethod
    def favorite_ranking(show_all = False):
        
        if show_all:
            join = 'RIGHT'
        else:
            join = 'INNER'
        
        query = "SELECT uf.club_id, c.name, COUNT(club_id) qty FROM pc_user_favorites uf " + join + " JOIN pc_clubs c ON c.id = uf.club_id GROUP BY c.id ORDER BY qty DESC, c.name;"
    
        dbcursor.execute (query)
        
        result = dbcursor.fetchall()
        
        #if no rows return, it means that it has not been favorited by anybody
        if (result == None):
            return "No clubs have been liked yet... go like some!"
        
        clubs_rank = []
                
        for club in result:
            clubs_rank.append([club[1],club[2]])
        
        return clubs_rank
    
    #method used to display club information on screen
    @staticmethod
    def str_convert(clubs):
        result = []
                    
        if clubs == None:
            result = "No clubs found"
        else:
            for club in clubs:
                result.append(json.dumps(club.__dict__))
            
        return str(result)    
          
      
