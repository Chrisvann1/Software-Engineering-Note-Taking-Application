import os
import shutil
import string
import time
import apiCalls
import json 
import requests

# Base frontend functionality
def clearConsole():
	os.system('cls' if os.name == 'nt' else 'clear')

def getConfig(line):
	# Line 2 is Primary color, 4 is Secondary color, 6 is pro mode
	with open('config.txt', 'r') as file:
		lines = file.readlines()
	# Reads the line looked at (non-array indexing)
	return lines[(line - 1)]

def setConfig(line, newContent):
	with open('config.txt', 'r') as file:
		lines = file.readlines()
	lines[(line-1)] = str(newContent) + '\n'
	with open('config.txt', 'w') as file:
		file.writelines(lines)

def optionColors():
	for i in range(0,255):
		print(f"\033[38;5;{str(i)}m{i}\033[0m", end = "\n" if i == 254 else ", "
)

def printColor(text, color, tail = "\n"):
	color = str(color)
	print(f"\033[38;5;{color}m{text}\033[0m", end = tail)

def lineBreak(columns, color):
	line = '-'
	for i in range(1,columns):
		line += '-'
	printColor(line, color, "")

def translation(response_string):
	text = ""
	inside_quotes = False
	new_line_check = False

	for num_str in response_string:
		num = num_str
        
		if num == 34:  # ASCII code for double quotation mark (")
			inside_quotes = not inside_quotes
		elif inside_quotes:
			text += chr(num)
			new_line_check = True
		elif new_line_check:
			text += "\n"
			new_line_check = False
    
	return text

# States of operation
def printStartScreen():
	columns = shutil.get_terminal_size()[0]
	lineBreak(columns, getConfig(4))
	printColor("Welcome to appName, select what you want to do", getConfig(2), "")
	lineBreak(columns, getConfig(4))
	print("\n")
	printColor("0. Exit APPNAME", 15)
	printColor("1. Open app", 15)
	printColor("2. Settings", 15)
	printColor("3. Help", 15)

def printAppUse():
	columns = shutil.get_terminal_size()[0]
	lineBreak(columns, getConfig(4))
	printColor("AppUse", getConfig(2))
	lineBreak(columns, getConfig(4))
	printColor("0. Go back", getConfig(2),"")
	printColor("1. New Note", getConfig(2),"")
	printColor("2. Edit Note(Limited Functionality in v0.01)", getConfig(2),"")
	printColor("3. Search Notes",getConfig(2),"")
	printColor("4. List Notes",getConfig(2),"")
	printColor("5. Delete Note",getConfig(2))
	printColor("6. Export Note to PDF", getConfig(2), "")

	

def printSettings():
	columns = shutil.get_terminal_size()[0]
	lineBreak(columns, getConfig(4))
	printColor("Settings", 15, "\n")
	printColor("To edit, enter the number of the feature you wish to edit.", 15)
	lineBreak(columns, getConfig(4))
	printColor("0. Go back", 15)
	printColor("1. Pro mode: " + getConfig(6), 15, "")
	printColor("2. Change Primary Color (WARNING: Opens a menu)", 15)
	printColor("3. Change Secondary Color (WARNING: Opens a menu)", 15)

def printHelpScreen():
	columns = shutil.get_terminal_size()[0]
	lineBreak(columns,getConfig(4))
	printColor("Help", getConfig(2))
	printColor("Version: v0.01", getConfig(2))
	printColor("If this is your first time using appName in a long while, it is recommended to check the github at https://github.com/Chrisvann1/Software-Engineering-Note-Taking-Application/ for updates.", getConfig(2))
	printColor("Found issues can be reported at the github link.", getConfig(2))
	printColor("Go to settings on the homepage to change color and to turn off/on Pro mode.", getConfig(2))
	printColor("Function Help:", getConfig(2))
	lineBreak(columns, getConfig(4))
	printColor("0. Go back", 15)



# The runtime funciton, (acts as a main loop)
def runtime(state):
	while(True):
		clearConsole()
		columns = shutil.get_terminal_size()[0]
		match (state):
	#Close app
			case -1:
				clearConsole()
				return
			
	# Start page
			case 0:
				printStartScreen()

			case 10 | 20 | 30:
				printStartScreen()
				state = 0

	# Application-in-use page
			case 1:
				printAppUse()

			case 110 | 120 | 130 | 140 | 150:
				printAppUse()
				state = 1

	#newNote
			case 11:
				lineBreak(columns, getConfig(4))
				printColor("Creating note...", getConfig(2))
				lineBreak(columns, getConfig(4))
				printColor("What would you like to name your new note?",getConfig(2), "")
				newNoteName = input(": ")
				printColor("What content would you like to add to start? (If you wish to add content later, enter '*END'.)", getConfig(2),"")
				printColor("*END: Stop typing to file. (Needs to be on its own line)",getConfig(2),"")
				printColor("return key: start a new line.",getConfig(2),"\n")
				newContent1 = []
				while True: 
					notes = input("")
					if notes == "*END":
						break
					newContent1.append(notes)
				newContent = ""
				for line in newContent1: 
					newContent += line + "\n"
				apiCalls.createNote(newNoteName,newContent)
				printColor("Would you like to add any tags? (Seperate tags with commas. If none or you wish to add later, enter 'none'.)",getConfig(2),"")
				newTags = input(": ")
				newTagList = newTags.split(",")
				if(newTags == 'none'):
					lineBreak(columns, getConfig(4))
					printColor("Note Created!",getConfig(2))
					time.sleep(2)
					clearConsole()
					printAppUse()
					state = 1
				else:
					apiCalls.addTag(newNoteName,newTagList)
					lineBreak(columns,getConfig(4))
					printColor("Note Created!", getConfig(2))
					time.sleep(2)
					clearConsole()
					printAppUse()
					state = 1
				
	#editNote
			case 12:
				lineBreak(columns, getConfig(4))
				printColor("Editing a note...",getConfig(2))
				lineBreak(columns, getConfig(4))
				printColor("0. Go back",getConfig(2),"")
				printColor("1. Add Content",getConfig(2),"")
				printColor("2. Edit Content (temporarily not working. Coming in v0.02)",getConfig(2),"")
				printColor("3. Add tags to note",getConfig(2),"")
				printColor("4. Delete tags from note", getConfig(2))





			case 16:
				lineBreak(columns, getConfig(4))
				printColor("Exporting note to PDF...", getConfig(2))
				lineBreak(columns,getConfig(4))
				printColor("Enter the name of the note to want to export.", getConfig(2), "")
				note_title = input(": ")

				#making API call to export note eto PDF

				url = "http://127.0.0.1:5000/notes/export"
				header = {'content-type': 'application/json'}
				response = requests.post(url, headers = header, json={'title': note_title})

				if response.status_code == 200:

					pdf_filename = f"{note_title}.pdf"
					with open(pdf_filename, 'wb') as file:
						file.write(response.content)
				else:
					printColor("Failed to export note to PDF.", getConfig(2))

				time.sleep(2)
				clearConsole()
				printAppUse()
				state = 1		



				
		#addContent
			case 121:
				lineBreak(columns, getConfig(4))
				printColor("Adding content...",getConfig(2))
				lineBreak(columns, getConfig(4))
				printColor("What is the name of the note you wish to add to?",getConfig(2),"")
				contentName = input(": ")
				printColor("Write the content to wish to add.",getConfig(2),"")
				printColor("*END: Stop typing to file.",getConfig(2),"")
				printColor("return key: start a new line.",getConfig(2),"")
				addContent1 = []
				while True: 
					notes = input("")
					if notes == "*END":
						break
					addContent1.append(notes)
				for line in addContent1: 
					addContent += line + "\n"
				apiCalls.addContent(contentName,addContent)
				lineBreak(columns, getConfig(4))
				printColor("Added content!",getConfig(2))
				time.sleep(2)
				clearConsole()
				printAppUse()
				state = 1
				
		#editContent limited/cut temporarily for time
			case 122:
				lineBreak(columns, getConfig(4))
				printColor("Coming in v0.02.",getConfig(2))
				lineBreak(columns, getConfig(4))
				time.sleep(2)
				clearConsole()
				printAppUse()
				state = 1

		#addTag
			case 123:
				lineBreak(columns, getConfig(4))
				printColor("Adding tag...",getConfig(2),"")
				lineBreak(columns, getConfig(4))
				printColor("What is the name of the note you wish to edit?",getConfig(2),"")
				addTagName = input(": ")
				printColor("What is the tags that you wish to add? (List with commas inbetween)", getConfig(2),"")
				addTags = input(": ")
				tagsList = addTags.split(",")
				apiCalls.addTag(addTagName,tagsList)
				lineBreak(columns, getConfig(4))
				printColor("Added tag(s)!", getConfig(2))
				time.sleep(2)
				clearConsole()
				printAppUse()
				state = 1

		#deleteTag
			case 124:
				lineBreak(columns, getConfig(4))
				printColor("Deleting tag...",getConfig(2),"")
				lineBreak(columns, getConfig(4))
				printColor("What is the name of the note you wish to edit?",getConfig(2),"")
				delTagName = input(": ")
				printColor("What is the tags that you wish to delete? (List with commas inbetween)", getConfig(2),"")
				delTags = input(": ")
				delTagsList = delTags.split(",")
				apiCalls.deletetag(delTagName,delTagsList)
				lineBreak(columns, getConfig(4))
				printColor("Deleted tag(s)!",getConfig(2))
				time.sleep(2)
				clearConsole()
				printAppUse()	
				state = 1

	#searchNotes
			case 13:
				lineBreak(columns, getConfig(4))
				printColor("What do you want to search by?",getConfig(2))
				lineBreak(columns, getConfig(4))
				printColor("0. Go back",getConfig(2),"")
				printColor("1. By title", getConfig(2),"") 
				printColor("2. By created date",getConfig(2),"") 
				printColor("3. By modified date",getConfig(2)) 

			case 1310 | 1320 | 1330 | 1340:
				printAppUse()
				state = 1

		#title
			case 131:
				lineBreak(columns, getConfig(4))
				printColor("Enter title to search.",getConfig(2))
				lineBreak(columns, getConfig(4))
				search_by = input(": ")
				desired_response = ['title','content','modified_date','created_date']
				api_response = apiCalls.searchNotes('title', search_by, desired_response)
				entries = translation(api_response.content)
				entries = entries.replace(r'\n', '\n')
				print (entries)
				
		#created_date
			case 132:
				lineBreak(columns, getConfig(4))
				printColor("Enter the beginning of the date range to search by.",getConfig(2))
				lineBreak(columns, getConfig(4))
				start = input(": ")
				lineBreak(columns, getConfig(4))
				printColor("Enter the end of the date range to search by.",getConfig(2))
				lineBreak(columns, getConfig(4))
				end = input(": ")
				desired_response = ['title','content','modified_date','created_date']
				api_response = apiCalls.searchNotes('created_date', "", desired_response, start, end)
				entries = translation(api_response.content)
				entries = entries.replace(r'\n', '\n')
				print(entries)

		#modified_date
			case 133:
				lineBreak(columns, getConfig(4))
				printColor("Enter the beginning of the date range to search by.",getConfig(2))
				lineBreak(columns, getConfig(4))
				start = input(": ")
				lineBreak(columns, getConfig(4))
				printColor("Enter the end of the date range to search by.",getConfig(2))
				lineBreak(columns, getConfig(4))
				end = input(": ")
				desired_response = ['title','content','modified_date','created_date']
				api_response = apiCalls.searchNotes('modified_date', "", desired_response, start, end)
				entries = translation(api_response.content)
				entries = entries.replace(r'\n', '\n')
				print(entries)
				
		#search by tag
			case 134: 
				printColor("Enter tag to search.", getConfig(2))
				lineBreak(columns, getConfig(4))
				search_by = input(": ")
				desired_response = ['title', 'content', 'modified_date', 'created_date', 'tag']
				api_response = apiCalls.searchNotesByTag(search_by, desired_response)
				entries = translation(api_response.content)
				entries = entries.replace(r'\n', '\n')
				print(entries)

	#listNotes
			case 14:
				lineBreak(columns, getConfig(4))
				printColor("Listing notes...",getConfig(2))
				lineBreak(columns, getConfig(4))
				printColor("0. Go back",getConfig(2),"")
				printColor("1. By title",getConfig(2),"")
				printColor("2. By created date",getConfig(2),"")
				printColor("3. By modified date",getConfig(2),"")
				printColor("4. List Tags (Coming soon! Not ready yet)", getConfig(2))


			case 1410 | 1420 | 1430 | 1440:
				printAppUse()
				state = 1

		#list notes by title
			case 141:
				lineBreak(columns, getConfig(4))
				printColor("Listing notes by title...",getConfig(2))
				lineBreak(columns, getConfig(4))
				gotList = apiCalls.listNotes("title")
				
				#printing the response
				entries = translation(gotList.content)
				print(entries)
				#for i in range(0,len(gotList.content)):
				#1	print(gotList.content[i], end = " ")

		#list notes by created date
			case 142:
				lineBreak(columns, getConfig(4))
				printColor("Listing notes by created date...",getConfig(2))
				lineBreak(columns, getConfig(4))
				gotList = apiCalls.listNotes("created_date")
				
				#printing the response
				entries = translation(gotList.content)
				print(entries)
				#for i in range(0,len(gotList.content)):
				#	print(gotList.content[i], end = " ")

		#list notes by modified date
			case 143:
				lineBreak(columns, getConfig(4))
				printColor("Listing notes by modified date...",getConfig(2))
				lineBreak(columns, getConfig(4))
				gotList = apiCalls.listNotes("modified_date")

				#printing the response
				entries = translation(gotList.content)
				print(entries)
				#for i in range(0,len(gotList.content)):
				#	print(chr(gotList.content[i]), end = "")
	
		#list tags	
			#case 144:
				#lineBreak(columns, getConfig(4))
				#printColor("Listing note tags...",getConfig(2))
				#lineBreak(columns, getConfig(4))
				#gotList = apiCalls.listTags()

				#printing the response
				#entries = translation(gotList.content)
				#print(entries)
				#for i in range(0,len(gotList.content)):
				#	print(chr(gotList.content[i]), end = "")

	#deleteNote
			case 15:
				lineBreak(columns, getConfig(4))
				printColor("Deleting note...", getConfig(2))
				lineBreak(columns, getConfig(4))
				printColor("Enter the name of the note you wish to delete.",getConfig(2),"")
				delNoteName = input(": ")
				apiCalls.deleteNote(delNoteName)
				printColor("Note deleted or it already does not exist", getConfig(2))
				time.sleep(2)
				clearConsole()
				printAppUse()
				state = 1

	# Settings page
			case 2:
				printSettings()
			
			case 210 | 220 | 230:
				printSettings()
				state = 2
		
		# Change status of pro mode
			case 21:
				print("Currently pro mode is " 
					+ "on" if int(getConfig(6)) == 1 else "off" 
					+ " to turn it " 
					+ "off" if int(getConfig(6)) == 1 else "on" 
					+ " enter" 
					+ "0" if int(getConfig(6)) == 1 else "1")
				response = input(": ")
				setConfig(6)
				clearConsole()
				lineBreak(columns, 15)
				printColor("Success, enter 0 to go back", getConfig(2))
				lineBreak(columns, 15)
			
		# Primary color selection
			case 22:
				lineBreak(columns, 15)
				print("Choose a primary color")
				printColor("current color", getConfig(2))
				lineBreak(columns, 15)
				optionColors()
				print("\n")
				lineBreak(columns, 15)
				printColor("To select, enter the number pertaining to the color you want.", 15)
				newColor = input(": ")
				setConfig(2,newColor)
				clearConsole()
				lineBreak(columns, getConfig(4))
				printColor("Success, enter 0 to go back", getConfig(2))
				lineBreak(columns, getConfig(4))

		# Secondary color selection
			case 23:
				lineBreak(columns, 15)
				print("Choose a secondary color")
				printColor("current color", getConfig(4))
				lineBreak(columns, 15)
				optionColors()
				print("\n")
				lineBreak(columns, 15)
				printColor("To select, enter the number pertaining to the color you want.", 15)
				newColor = input(": ")
				setConfig(4,newColor)
				clearConsole()
				lineBreak(columns, getConfig(4))
				printColor("Success, enter 0 to go back", getConfig(2))
				lineBreak(columns, getConfig(4))
			 # Rename a tag	
			case 27:
				printColor("Renaming a tag...", getConfig(2))
				lineBreak(columns, getConfig(4))
				printColor("Enter the current tag name:", getConfig(2))
				old_tag = input(": ")
				printColor("Enter the new tag name:", getConfig(2))
				new_tag = input(": ")
				apiCalls.renameTag(old_tag, new_tag)
				lineBreak(columns, getConfig(4))
				printColor("Tag renamed successfully!", getConfig(2))
				time.sleep(2)
				clearConsole()
				printSettings()
				state = 2
		# General Help page	
			case 3:
				printHelpScreen()

	# Fall through error case
			case 999:
				printColor("Invalid state", 9)
				break

		userInput = input(": ")
		if userInput != "":
			if (state == 0 and userInput == '0'):
				state = -1
			else:
				state = (state * 10) + int(userInput)


		userInput - input(": ")
		if userInput != "":
			if state == 0 and userInput == '0':
				state = -1
			else:
				state = (state * 10) + int(userInput)

# Runtime
runtime(0)

