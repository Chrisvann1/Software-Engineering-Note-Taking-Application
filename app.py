from flask import Flask 
import sqlite3
from flask import request, abort
from datetime import date, date, timedelta

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

#Used to create notes and create tags
@app.route('/create', methods=['POST'])
def create(): 
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    payload = request.json
    try: 
        title = payload.get('title')
    except KeyError:
        abort(206, "Data Entry Requires A Title")
    
    try: 
        content = payload.get('content')
    except KeyError: 
        content = ""
    
    try: 
        tags = payload.get('tag')
    except KeyError: 
        tags = ""
    
    if tags != "":
        for value in tags: 
            cursor.execute("INSERT INTO tags VALUES (?,?)", (title, value))
    
    else: 
        cursor.execute("INSERT INTO notes VALUES (?,?,?,?)", (title,content,date.today(),date.today()))

    conn.close()
        
     
#used to delete notes and delete tags
@app.route('/delete', methods=['POST'])
def delete():
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    payload = request.json
    try: 
        title = payload.get('title')
    except KeyError:
        abort(206, "Data Entry Requires A Title")
    
    try: 
        tags = payload.get('tag')
    except KeyError: 
        tags = ""
        
    if tags != "": 
        for tag in tags: 
            cursor.execute(f"DELETE FROM tags WHERE title == {title} AND tag == {tag}")
    else: 
        cursor.execute(f"DELETE FROM notes WHERE title == {title}")
    
    conn.close()

#used to update note content
@app.route('/update', methods=['POST'])
def update(): 
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    payload = request.json
    
    try: 
        title = payload.get('title')
    except KeyError:
        abort(206, "Data Entry Requires A Title")
        
    try: 
        content = payload.get('content')
    except KeyError: 
        abort(206, "Date Entry Requires Content")
        
    
    cursor.execute(f"UPDATE notes SET content = {content}, modified_date = {date.today()} WHERE title = {title}")
    conn.commit()
    conn.close()
    


###SEARCHING FUNCTIONS

#function for all search methods - modified date, tag, created date, etc.
#This function will also likely be used to return content which can be used for both 
#viewing content and PDF conversion
@app.route('/search', methods=['GET'])
def search():
    # requests must have the application/json content type
    # open connection, get the requests passed
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    payload = request.json # json dict
    search_field = payload.get('search_field') #string
    query = payload.get('query')
    return_fields = payload.get('return_fields')

    # field safety
    assert search_field in set(['modified_date', 'title', 'created_date', 'tag'])
    for field in return_fields:
        assert field in set(['modified_date', 'title', 'created_date', 'tag'])
    
    # we will always return title
    if "title" not in return_fields:
        # prepend
        return_fields.insert(0, "title")
    # pre-prepare the SELECT fields
    select_fields_string = "".join(['notes.' + field + ',' for field in return_fields])
    # let us rid ourselves of that pesky comma, shall we?
    select_fields_string = select_fields_string[:-1]

    # modified_date looks like 'YYYY-MM-DD'
    if search_field == 'modified_date':
        # beginning of day
        start = datetime.strptime(query, '%Y-%m-%d')
        # end of day
        end = start + timedelta(days=1)
        # into decimals then strings
        start = str(start.timestamp())
        end = str(end.timestamp())
        sql_query = f"""
                   SELECT {select_fields_string}
                   FROM notes
                   WHERE notes.modified_date > {start} AND notes.modified_date < {end}
                   """
    # title
    if search_field == 'title':
        sql_query = f"""
                   SELECT {select_fields_string}
                   FROM notes
                   WHERE notes.title = {query}
                   """
    # created_date looks like 'YYYY-MM-DD'
    if search_field == 'created_date':
        # beginning of day
        start = datetime.strptime(query, '%Y-%m-%d')
        # end of day
        end = start + timedelta(days=1)
        # into decimals then strings
        start = str(start.timestamp())
        end = str(end.timestamp())
        sql_query = f"""
                   SELECT {select_fields_string}
                   FROM notes
                   WHERE notes.created_date > {start} AND notes.created_date < {end}
                   """
    # tag (super hard ?)
    if search_field == 'tag':
        # gets the notes objects that match the tag search
        sql_query = f"""
                   SELECT {search_fields_string}
                   FROM notes
                   INNER JOIN tags AS tg
                   ON notes.title = tg.title
                   WHERE tg.tag = {query}
                   """
    cursor.execute(sql_query)
    fetch = cursor.fetchall()
    conn.close()
    return fetch

###LISTING FUNCTIONS
@app.route('/list', methods=['GET'])
def list():
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    # requests must have the application/json content type
    payload = request.json # json dict
     # {"list_field": "modified_date"}
    list_field = payload['list_field']
    assert list_field in set(['modified_date', 'title', 'created_date'])
    # handle the fact that title is always returned
    # and you will NOT be SQL injecting this shit
    if list_field == 'title':
        list_field = ','
    else:
        list_field = ", notes." + list_field
    sql_query = f"""
                   SELECT notes.title{list_field}
                   FROM notes
                   """
    cursor.execute(sql_query)
    
    fetch = cursor.fetchall()
    conn.close()
    return fetch  

def list_tags():
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    pass 
