import mysql.connector

#creates connection
mydb = mysql.connector.connect(
  host="localhost",
  user="penn_clubs",
  passwd="12345678",
  database="pc"
)

#creates cursor to access database
dbcursor = mydb.cursor()

#resets the database
def reset_db():
    query = "DELETE FROM pc_user_favorites WHERE id>0;"
    dbcursor.execute (query)
    
    query = "DELETE FROM pc_club_tags WHERE True;"
    dbcursor.execute (query)
    
    query = "DELETE FROM pc_tags WHERE True;"
    dbcursor.execute (query)
    
    query = "DELETE FROM pc_clubs WHERE id>0;"
    dbcursor.execute (query)
    
    query = "DELETE FROM pc_users WHERE True;"
    dbcursor.execute (query)
    mydb.commit()
    
