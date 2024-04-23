from flask import Flask 
import sqlite3
from flask import request, abort, jsonify
from datetime import date, date, timedelta, datetime
import os
import markdown 



app = Flask(__name__)

# called to initialize the SQL databse schema
def init_db(): 
    # name of db
    conn = sqlite3.connect("note.db")
    # cursors write to dbs
    cursor = conn.cursor()
    # schema for the notes table
    # notice the fields:
    cursor.execute("""CREATE TABLE IF NOT EXISTS notes(
    title TEXT,
    content TEXT, 
    modified_date INTEGER,
    created_date INTEGER,
    PRIMARY KEY(title))""")
    
    # schema for the tags table
    # notice the fields:
    cursor.execute("""CREATE TABLE IF NOT EXISTS tags(
        title TEXT, 
        tag TEXT,
        PRIMARY KEY(title,tag)
        FOREIGN KEY(title) REFERENCES notes(title)
    )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS images(
        title TEXT, 
        image TEXT,
        PRIMARY KEY(title,image)
        FOREIGN KEY(title) REFERENCES notes(title)
    )""")
    conn.close()
 
# call the above   
init_db()

#Creates a subdirectory called MKDown_dir if it does not exist
def init_markdown():
    os.makedirs("MKDown_dir", exist_ok=True)
init_markdown()

### CREATION AND DELETION FUNCTIONS

# Used to create notes
# pass HTTP POST request to /notes endpoint
# make sure you have Content-Type: application/json in the request header
# payload JSON should have the following fields:
# 'title' (required): string of note title
# 'content' (optional): string of note content
@app.route('/notes', methods=['POST'])
def create_note(): 
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    payload = request.json
    try: 
        title = payload.get('title')
        if title is None: 
            raise KeyError("Data Entry Requires A Title")
    except KeyError as error:
        abort(206, error)
        
    try: 
        content = payload.get('content')
    except KeyError: 
        content = ""
    
    cursor.execute("INSERT INTO notes VALUES (?,?,?,?)", (title,content,date.today(),date.today()))
    conn.commit()
    conn.close()

    return "Note Created Successfully", 200

#{"title": "information", "tag": ["things", "to", "do"]}
#We need to eventually develop a safeguard for this. We need to make
#sure that this title doesn't exist
#We can proabably do this in the second sprint if needed

# Used to write tag information to the tags table
# pass HTTP POST request to /tags endpoint
# Entries in tags table have fields (title, tag) 
# payload JSON should have the following fields:
# 'title' (required): string of note title
# 'tag' (required): string of note tag       
@app.route('/tags', methods=['POST'])
def create_tag(): 
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    payload = request.json
    try: 
        title = payload.get('title')
        if title is None: 
            raise KeyError("Data Entry Requires A Title")
    except KeyError as error:
        abort(206, error)

    try: 
        tags = payload.get('tag')
        if tags is None: 
            raise KeyError("Data Entry Requires a tag")
    except KeyError as error: 
        abort(206, error)
        
    for value in tags: 
        cursor.execute("INSERT INTO tags VALUES (?,?)", (title, value))
    
    conn.commit()
    conn.close()
    return "Tag(s) Created Successfully", 200

@app.route('/images', methods=['POST'])
def add_image(): 
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    payload = request.json
    try: 
        title = payload.get('title')
        if title is None: 
            raise KeyError("Data Entry Requires A Title")
    except KeyError as error:
        abort(206, error)

    try: 
        images = payload.get('image')
        if images is None: 
            raise KeyError("Data Entry Requires an Image")
    except KeyError as error: 
        abort(206, error)
        
    for value in images: 
        cursor.execute("INSERT INTO images VALUES (?,?)", (title, value))
    
    conn.commit()
    conn.close()
    return "Image(s) Added Successfully", 200
# used to delete notes
# pass HTTP DELETE request to /notes endpoint
# payload JSON should have the following fields:
# 'title' (required): string of note title
@app.route('/notes', methods=['DELETE'])
def delete_note():
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    payload = request.json
    try: 
        title = payload.get('title')
        if title is None: 
            raise KeyError("Data Entry Requires a title")
    except KeyError as error:
        abort(206, error)

    cursor.execute(f"DELETE FROM tags WHERE tags.title == '{title}'")
    cursor.execute(f"DELETE FROM notes WHERE notes.title == '{title}'")
    conn.commit()   
    conn.close()
    return "Note Deleted Successfully", 200

#for tags you need a list in json format
# used to delete tags
# pass HTTP DELETE request to /tags endpoint
# payload JSON should have the following fields:
# 'title' (required): string of note title
# 'tag' (required): string of note tag
# 'content' will be used in list format 
@app.route('/tags', methods=['DELETE'])
def delete_tag():
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    payload = request.json
    try: 
        title = payload.get('title')
        if title is None: 
            raise KeyError("Data Entry Requires a title")
    except KeyError as error:
        abort(206, error)
    
    try: 
        tags = payload.get('tag')
        if tags is None: 
            raise KeyError("Data Entry Requires a tag")
    except KeyError as error: 
        abort(206, error)
        
    for tag in tags: 
        cursor.execute(f"DELETE FROM tags WHERE title == '{title}' AND tag == '{tag}'")
    conn.commit()    
    conn.close()
    return "Tag(s) Deleted Successfully", 200

@app.route('/images', methods=['DELETE'])
def remove_image(): 
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    payload = request.json
    try: 
        title = payload.get('title')
        if title is None: 
            raise KeyError("Data Entry Requires a title")
    except KeyError as error:
        abort(206, error)
    
    try: 
        images = payload.get('image')
        if images is None: 
            raise KeyError("Data Entry Requires an image")
    except KeyError as error: 
        abort(206, error)
        
    for image in images: 
        cursor.execute(f"DELETE FROM images WHERE title == '{title}' AND tag == '{image}'")
    conn.commit()    
    conn.close()
    return "Image(s) Deleted Successfully", 200


# used to update note content
# pass HTTP PUT request to /notes endpoint
# payload JSON should have the following fields:
# 'title' (required): string of note title
# 'content' (required): string of note content
@app.route('/notes', methods=['PUT'])
def update_note(): 
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    payload = request.json
    
    try: 
        title = payload.get('title')
        if title is None: 
            raise KeyError("Data Entry Requires a title")
    except KeyError as error:
        abort(206, error)
        
    try: 
        content = payload.get('content')
        if content is None: 
            raise KeyError("Data Entry Requires content")
    except KeyError as error: 
        abort(206, error)
        
    cursor.execute(f"UPDATE notes SET content == '{content}', modified_date == '{date.today()}' WHERE title == '{title}'")
    conn.commit()
    conn.close()
    return "Content Updated Successfully", 200
    


###SEARCHING FUNCTIONS

#The "return field" needs to be a list"
# function for all search methods - modified date, tag, created date, etc.
# pass HTTP GET request to /notes/search endpoint
# 'search_field' (required): string representing note field to search by. must be exactly one of the following:
# - 'modified_date', 'title', 'created_date'
# 'query' (required): string representing the string to search for in the 'search_field'
# Note: searching by content will only return an exact match
# 'return_fields' (required): list of strings representing aspects of the notes you want returned back to you
# must be zero or more of 'modified_date', 'title', 'created_date', 'content'

# This function will also likely be used to return content which can be used for both 
# viewing content and PDF conversion
@app.route('/notes/search', methods=['GET'])
def search_notes():
    # requests must have the application/json content type
    # open connection, get the requests passed
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    payload = request.json # json dict
    search_field = payload.get('search_field') #string
    print(search_field)
    query = payload.get('query')
    return_fields = payload.get('return_fields')

    # field safety
    assert search_field in set(['modified_date', 'title', 'created_date','content'])
    for field in return_fields:
        assert field in set(['modified_date', 'title', 'created_date','content'])
    
    # we will always return title
    if "title" not in return_fields:
        # prepend
        return_fields.insert(0, "title")
    # pre-prepare the SELECT fields
    select_fields_string = "".join(['notes.' + field + ',' for field in return_fields])
    # let us rid ourselves of that pesky comma, shall we?
    select_fields_string = select_fields_string[:-1]

    if search_field == 'content':
        sql_query = f"""
                    SELECT {select_fields_string}
                    FROM notes 
                    WHERE notes.content == '{query}'
                    """
    # modified_date looks like 'YYYY-MM-DD'
    if search_field == 'modified_date':
        start = datetime.strptime(query, '%Y-%m-%d')

        # Construct SQL query
        sql_query = f"""
                     SELECT {select_fields_string} FROM notes 
                     WHERE created_date == '{start.strftime('%Y-%m-%d')}'
                     """
    # title
    if search_field == 'title':
        sql_query = f"""
                   SELECT {select_fields_string}
                   FROM notes
                   WHERE notes.title == '{query}'
                   """
    # created_date looks like 'YYYY-MM-DD'
    if search_field == 'created_date':
        start = datetime.strptime(query, '%Y-%m-%d')
        # Construct SQL query
        sql_query = f"""
                     SELECT {select_fields_string} FROM notes 
                     WHERE created_date >= '{start.strftime('%Y-%m-%d')}'
                     """

    # tag (super hard ?)
    if search_field == 'tag':
        # gets the notes objects that match the tag search
        sql_query = f"""
                   SELECT {select_fields_string}
                   FROM notes
                   INNER JOIN tags AS tg
                   ON notes.title == tg.title
                   WHERE tg.tag == '{query}'
                   """
    cursor.execute(sql_query)
    fetch = cursor.fetchall()
    conn.close()
    return jsonify(fetch)


@app.route('/tags/search', methods=['GET'])
def search_tags():
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    payload = request.json
    
    query = payload.get('query')
    
    sql_query = f"""
                SELECT tags.title, tags.tag
                FROM tags
                WHERE tags.tag == '{query}'
                """
                
    cursor.execute(sql_query)
    fetch = cursor.fetchall()
    conn.close()
    return jsonify(fetch)
    
    # title

#{"list_field":"title"}
###LISTING FUNCTIONS
# function to list return all notes. only returns the title and 'list_field' of all the notes.
# Ex: if 'list field' is 'content' we return the content and title of every note.
# pass HTTP GET request to /notes/list endpoint
# 'list_field' (optional): string representing note field to list by. always lists by at least title.
# - supports 'modified_date', 'title', 'created_date'

@app.route('/notes/list', methods=['GET'])
def list():
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    # requests must have the application/json content type
    payload = request.json # json dict
     # {"list_field": "modified_date"}
    list_field = payload['list_field']
    assert list_field in set(['modified_date', 'title', 'created_date'])
    # handle the fact that title is always returned
    # and you will NOT be SQL injecting this shit (try me trent)
    if list_field == 'title':
        list_field = ''
        sql_query = f"""
            SELECT notes.title{list_field}
            FROM notes ORDER BY UPPER(notes.title)
            """
    elif list_field == 'modified_date':
        list_field = ", notes." + list_field
        sql_query = f"""
        SELECT notes.title{list_field}
        FROM notes ORDER BY notes.modified_date
        """
    else:
        list_field = ", notes." + list_field
        sql_query = f"""
                    SELECT notes.title{list_field}
                    FROM notes ORDER BY notes.created_date
                    """
    cursor.execute(sql_query)
    
    fetch = cursor.fetchall()
    conn.close()
    return jsonify(fetch) 

@app.route('/tags/list', methods=['GET'])
def list_tags():
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    sql_query = f"""
                    SELECT tags.tag, tags.title
                    FROM tags ORDER BY UPPER(tags.tag)
                """
    cursor.execute(sql_query)
    
    fetch = cursor.fetchall()
    conn.close()
    return jsonify(fetch)

@app.route('/mkdown', methods=['POST'])
def markdown_conversion_folder(): 
    payload = request.json
    try: 
        title = payload.get('title')
        if title is None: 
            raise KeyError("Data Conversion Requires a title")
    except KeyError as error:
        abort(206, error)
        
    try: 
        content = payload.get('content')
        if content is None: 
            raise KeyError("Data Conversion Requires content")
    except KeyError as error: 
        abort(206, error)
        
    with open("./MKDown_dir/" + title, "w") as mk: 
        mk.write(markdown.markdown(content))
    
     
app.run(debug=True)

@app.route('/notes/export', methods=['POST'])
def export_note_to_pdf():
    payload = request.json
    title = payload.get('title')
    if title is None:
        abort(400, 'Title is required')

    #retrieve note from the database based on its title
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE title = ?", (title,))
    note = cursor.fetchone()
    conn.close()

    if note is None:
        abort(404, 'Note not found')

    #generates the PDF using reportLab

    from reportlab.pdfgen import canvas

    pdf_filename - f"{title}.pdf"
    c = canvas.Canvas(pdf_filename)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, note[0])  # Title
    c.drawString(100, 700, note[1])  # Content

    c.showPage()
    c.save()

    return send_file(pdf_filename, as_attachment = True)




