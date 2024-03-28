from flask import Flask 
import sqlite3 

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
def search_by_title():
    pass 

#function to search by modified date
def search_by_modified_date():
    pass 

#function to search by created date
def search_by_created_date():
    pass

#function to search by tag
def search_by_tag(): 
    pass



###LISTING FUNCTIONS

def list_by_title():
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    cursor.execute(f"""
                   SELECT notes.title
                   FROM notes
                   """)
    
    titles = cursor.fetchall()
    for value in titles: 
        print(value)
    conn.close()
    return titles 

def list_by_modified_date():
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    cursor.execute(f"""
                   SELECT notes.title, notes.modified_date
                   FROM notes
                   """)
    
    modified_date = cursor.fetchall()
    conn.close()
    return modified_date 



def list_by_created_date():
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    cursor.execute(f"""
                   SELECT notes.title, notes.created_date
                   FROM notes
                   """)
    
    created_date = cursor.fetchall()
    conn.close()
    return created_date 

def list_tags():
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()