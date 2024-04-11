import requests

# Http integration managment
# generic verion of a http request, formats to request well.
def request():
	pass

# generic version of a http response, formats to respond well.
def response():
	pass

header = "Content-Type: application/json"

# Note Searching
def listNotes():
	#by created date, modified date, title
	pass

def searchNotes():
	#by content, title, tags, date
	pass



# Note Classification Suite
def addTag(noteTitle, tagName):
	# Makes a list of tags that should be added to the title, does not need to check if tags exist
    url = "http://127.0.0.1:5000/tags"
    requests.post(url,headers=header, data={'title': noteTitle, 'tag': tagName})

def deletetag(noteTitle, tagName):
	# Delete a tag from a note
	url = "http://127.0.0.1:5000/tags"
	requests.delete(url,headers=header, data={'title': noteTitle, 'tag': tagName})

def listTags():
	# Lists tags of all notes
	pass 



# Note creation suite
def createNote(noteTitle, noteContent):
	url = "http://127.0.0.1:5000/notes"
	requests.post(url,headers=header, data={'title': noteTitle, 'content': noteContent}) 

def deleteNote(noteTitle, noteContent):
	url = "http://127.0.0.1:5000/notes"
	requests.delete(url,headers=header, data={'title': noteTitle, 'content': noteContent}) 

def addContent(noteTitle):
	# This should add to an existing note
	url = "http://127.0.0.1:5000/notes"
	requests.put(url,headers=header, data={'title': noteTitle}) 


def main():
	nTitle = "test note"
	nContent = "This is the note"
	tName = "test tag"
	createNote(nTitle, nContent)

main()