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



# Note creation suite
def createNote(noteTitle, noteContent):
	url = "http://127.0.0.1:5000/notes"
	return requests.post(url,headers=header, json={'title': noteTitle, 'content': noteContent}) 

def deleteNote(noteTitle):
	url = "http://127.0.0.1:5000/notes"
	return requests.delete(url,headers=header, json={'title': noteTitle}) 

def addContent(noteTitle, noteContent):
	# This should add to an existing note
	url = "http://127.0.0.1:5000/notes"
	return requests.put(url,headers=header, json={'title': noteTitle, 'content': noteContent}) 

def main():
	listCo = 'title'
	title = "title1"
	content = "content1"
	mContent = "more content"

	createNote(title,content)
	addContent(title, mContent)

	title = "title2"
	content = "content2"
	createNote(title,content)

	# tag = "testTag"
	# addTag(title, tag)

	r = listNotes(listCo)
	print(r.content)	
	
	searchBy = ['title','content']
	r = searchNotes('title', 'title1', searchBy)
	print(r.content)


main()