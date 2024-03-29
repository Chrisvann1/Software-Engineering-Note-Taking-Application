from flask import Flask 
import sqlite3
from flask import request

app = Flask(__name__)


def init_db(): 
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS notes(
    id INTEGER,
    title TEXT,
    content TEXT, 
    modified_date INTEGER,
    created_date INTEGER,
    PRIMARY KEY(title))""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS tags(
        title TEXT, 
        tag TEXT,
        PRIMARY KEY(title,tag)
        FOREIGN KEY(title) REFERENCES notes(title)
    )""")
    
    conn.close()
    
init_db()

###CREATION AND DELETION FUNCTIONS

#Function to create a note
def create_note(): 
    pass 

#function to delete a note
def delete_note():
    pass

#function to create a tag
def create_tag(): 
    pass

#function to delete a tag
def delete_tag():
    pass 

#function to add content
#I do not know if we need a separate function for edit content. I can explain the reasoning in class 
def add_content(): 
    pass 


###SEARCHING FUNCTIONS

#This will be called by the frontend for two different functions
    #1) Viewing Content 
    #2) PDF Conversion 
def return_content():
    pass 

#function to search by title
@app.route('/search', methods=['GET'])
def search():
    # requests must have the application/json content type
    payload = request.json # json dict
    search_field = payload['search_field'] #string
    query = payload['query']
    return_fields = payload['return_fields']
    assert search_field in set(['modified_date', 'title', 'created_date', 'tag'])
    pass

###LISTING FUNCTIONS
@app.route('/list', methods=['GET'])
def list():
    # requests must have the application/json content type
    payload = request.json # json dict
    list_field = payload['list_field']
    assert list_field in set(['modified_date', 'title', 'created_date'])
    # handle the fact that title is always returned
    if list_field is 'title':
        list_field = ','
    else:
        list_field = ", notes." + list_field
    sql_query = f"""
                   SELECT notes.title{list_field}
                   FROM notes
                   """
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    cursor.execute(sql_query)
    
    fetch = cursor.fetchall()
    conn.close()
    return fetch  

def list_tags():
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()