from flask import Flask, request, abort, jsonify
import sqlite3
from datetime import date

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS notes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE,
    content TEXT,
    modified_date INTEGER,
    created_date INTEGER)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS tags(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        tag TEXT,
        FOREIGN KEY(title) REFERENCES notes(title))""")

    conn.close()

init_db()

@app.route('/notes', methods=['POST'])
def create_note():
    payload = request.json
    title = payload.get('title')
    content = payload.get('content', "")

    if not title:
        abort(400, "Title is required")

    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO notes (title, content, modified_date, created_date) VALUES (?, ?, ?, ?)",
                       (title, content, date.today(), date.today()))
        conn.commit()
    except sqlite3.IntegrityError:
        abort(400, "Note with the same title already exists")
    finally:
        conn.close()

    return jsonify({"message": "Note created successfully"}), 201

@app.route('/notes/<title>', methods=['PUT'])
def update_note(title):
    payload = request.json
    content = payload.get('content')

    if not content:
        abort(400, "Content is required")

    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET content = ?, modified_date = ? WHERE title = ?",
                   (content, date.today(), title))
    conn.commit()
    conn.close()

    return jsonify({"message": "Note updated successfully"})

@app.route('/notes/<title>', methods=['DELETE'])
def delete_note(title):
    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE title = ?", (title,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Note deleted successfully"})

@app.route('/tags', methods=['POST'])
def create_tag():
    payload = request.json
    title = payload.get('title')
    tag = payload.get('tag')

    if not title or not tag:
        abort(400, "Title and tag are required")

    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tags (title, tag) VALUES (?, ?)", (title, tag))
    conn.commit()
    conn.close()

    return jsonify({"message": "Tag created successfully"}), 201

@app.route('/tags/<title>', methods=['DELETE'])
def delete_tag(title):
    payload = request.json
    tag = payload.get('tag')

    if not tag:
        abort(400, "Tag is required")

    conn = sqlite3.connect("note.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tags WHERE title = ? AND tag = ?", (title, tag))
    conn.commit()
    conn.close()

    return jsonify({"message": "Tag deleted successfully"})

@app.route('/notes/search', methods=['GET'])
def search_notes():
    payload = request.json
    search_field = payload.get('search_field')
    query = payload.get('query')
    return_fields = payload.get('return_fields')

    if not search_field or not query:
        abort(400, "Search field and query are required")

    if search_field not in ['modified_date', 'title', 'created_date', 'tag']:
        abort(400, "Invalid search field")

    # Implement the search logic based on the search_field and query

@app.route('/notes', methods=['GET'])
def list_notes():
    payload = request.json
    list_field = payload.get('list_field')

    if not list_field:
        abort(400, "List field is required")

    if list_field not in ['modified_date', 'title', 'created_date']:
        abort(400, "Invalid list field")

    # Implement the listing logic based on the list_field

@app.route('/tags', methods=['GET'])
def list_tags():
    # Implement the logic to list all tags
    pass
