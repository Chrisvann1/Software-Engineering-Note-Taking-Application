import requests

# Http integration managment
# generic verion of a http request, formats to request well.
def request():
	pass

# generic version of a http response, formats to respond well.
def response():
	pass

header = {'Content-Type': 'application/json'}

# Note Searching
def listNotes(listBy):
	#by created date, modified date, title
	url = "http://127.0.0.1:5000/notes/list"
	return requests.get(url,headers=header, json={'list_field': listBy})

def searchNotes(field, searchQuery, returnField):
	#by content, title, tags, date
	url = "http://127.0.0.1:5000/notes/search"
	return requests.get(url,headers=header, json={'search_field': field, 'query': searchQuery, 'return_fields': returnField})
	
def searchNotesByTag(tag, returnFields):
    # Search notes by tag
    url = "http://127.0.0.1:5000/tags/search"
    return requests.get(url, headers=header, json={'query': tag, 'return_fields': returnFields})



# Note Classification Suite
def addTag(noteTitle, tagName):
	# Makes a list of tags that should be added to the title, does not need to check if tags exist
    url = "http://127.0.0.1:5000/tags"
    return requests.post(url,headers=header, json={'title': noteTitle, 'tag': tagName})

def deletetag(noteTitle, tagName):
	# Delete a tag from a note
	url = "http://127.0.0.1:5000/tags"
	return requests.delete(url,headers=header, json={'title': noteTitle, 'tag': tagName})

def listTags():
	# Lists tags of all notes
	pass 
	
def renameTag(oldTag, newTag):
    # Rename a tag
    url = "http://127.0.0.1:5000/tags/rename"
    return requests.put(url, headers=header, json={'old_tag': oldTag, 'new_tag': newTag})

def searchTags(query):
	#searches tags
	url = "http://127.0.0.1:5000/tags/search"
	return requests.get(url,headers=header, json={'query': query})



# Note creation suite
def createNote(noteTitle, noteContent):
	url = "http://127.0.0.1:5000/notes"
	return requests.post(url,headers=header, json={'title': noteTitle, 'content': noteContent}) 

def deleteNote(noteTitle):
	url = "http://127.0.0.1:5000/notes"
	return requests.delete(url,headers=header, json={'title': noteTitle}) 

def addContent(noteTitle, noteContent):
	url = "http://127.0.0.1:5000/notes"
	return requests.put(url,headers=header, json={'title': noteTitle, 'content': noteContent}) 

def mdDownConversion(noteTitle, noteContent): 
    url = "http://127.0.0.1:5000/mkdown"
    return requests.post(url, headers=header, json={'title': noteTitle, 'content': noteContent})

def mainTest():
	listCo = 'title'
	title = "Btitle1"
	content = "content1"
	mContent = "more content"

	createNote(title,content)
	addContent(title, mContent)

	title = "Atitle2"
	content = "content2"
	createNote(title,content)

	# tag = "testTag"
	# addTag(title, tag)

	r = listNotes(listCo)
	print(r.content)	
	
	searchBy = ['title','content']
	r = searchNotes('title', 'title1', searchBy)
	print(r.content)
