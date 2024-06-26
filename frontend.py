
import os
import shutil
import string
import time
import apiCalls
import json 
import requests
import easygui

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
        print(f"\033[38;5;{str(i)}m{i}\033[0m", end = "\n" if i == 254 else ", ")

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

def input_pre_filled(prompt, prefill):
	#Pass a prompt as if operating a normal input() statement and then a prefill which will fill the text box.
	input = ""
	# assert input == type("String")
	input = easygui.enterbox(prompt, title="Input", default = prefill)
	if input is None:
		input = prefill
		#returns the input from the user in the form of a string
		return input

# States of operation
def printStartScreen():
    columns = shutil.get_terminal_size()[0]
    lineBreak(columns, getConfig(4))
    printColor("Welcome to NOTEWORTHY, select what you want to do", getConfig(2), "")
    lineBreak(columns, getConfig(4))
    print("\n")
    printColor("0. Exit NOTEWORTHY", 15)
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
	printColor("2. Edit Note", getConfig(2),"")
	printColor("3. Search Notes",getConfig(2),"")
	printColor("4. List Notes",getConfig(2),"")
	printColor("5. Delete Note",getConfig(2),"")
	printColor("6. Tag Menu", getConfig(2),"")
	printColor("7. Convert Note to MKDown",getConfig(2))


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
	printColor("Version: v0.02", getConfig(2))
	printColor("If this is your first time using Noteworthy in a long while, it is recommended to check the github at https://github.com/Chrisvann1/Software-Engineering-Note-Taking-Application/ for updates.", getConfig(2))
	printColor("Found issues can be reported at the github link.", getConfig(2))
	printColor("Go to settings on the homepage to change color and to turn off/on Pro mode.", getConfig(2))
	printColor("Function Help:", getConfig(2))
	printColor("Date format: YYYY-MM-DD", getConfig(2),"")
	printColor("Be careful when selecting an option as escaping without running the function is currently not possible.", getConfig(2),"")
	printColor("Make sure when adding tags you seperate them by commas.", getConfig(2),"")


	lineBreak(columns, getConfig(4))
	printColor("0. Go back", 15)
  
def printTagMenu():
    columns = shutil.get_terminal_size()[0]
    lineBreak(columns, getConfig(4))
    printColor("Tag Management", getConfig(2))
    lineBreak(columns, getConfig(4))
    printColor("0. Go back", getConfig(2), "")
    printColor("1. Add a tag", getConfig(2), "")
    printColor("2. Delete a tag", getConfig(2), "")
    printColor("3. List all tags", getConfig(2), "")
    printColor("4. Search for a tag", getConfig(2), "")
    printColor("5. Rename a tag", getConfig(2))
    
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

			case 110 | 120 | 130 | 140 | 150 | 160 | 170:
				printAppUse()
				state = 1

		#newNote
			case 11:
				lineBreak(columns, getConfig(4))
				printColor("Creating note...", getConfig(2))
				lineBreak(columns, getConfig(4))
				printColor("What would you like to name your new note?",getConfig(2), "")
				newNoteName = input(": ")
				while newNoteName == "":
					printColor("The notes name cannot be empty. Please input a name.", getConfig(2))
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
				printColor("Would you like to add any tags? (Seperate tags with commas and a space. If none or you wish to add later, enter 'none'.)",getConfig(2),"")
				newTags = input(": ")
				while newTags != 'none' and not all(tag.strip() for tag in newTags.split(',')):
					printColor("Tags should be separated by commas and a space. Please enter tags in the correct format.", getConfig(2))
					newTags = input(": ")
				newTagList = newTags.split(", ")
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
				printColor("1. New Content",getConfig(2),"")
				printColor("2. Edit Content",getConfig(2),"")
				printColor("3. Add tags to note",getConfig(2),"")
				printColor("4. Delete tags from note", getConfig(2))	


				
		#addContent
			case 121:
				lineBreak(columns, getConfig(4))
				printColor("Adding new content...",getConfig(2))
				lineBreak(columns, getConfig(4))
				printColor("What is the name of the note you wish to change?",getConfig(2),"")
				contentName = input(": ")
				while contentName == "":
					printColor("The note name cannot be empty. Please input a valid name.",getConfig(2))
					contentName = input(": ")
				printColor("Write the content to wish to add.",getConfig(2),"")
				printColor("*END: Stop typing to file.",getConfig(2),"")
				printColor("return key: start a new line.",getConfig(2),"")
				addContent1 = []
				addContent = ""
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
				
		#editContent
			
			case 122:
				lineBreak(columns, getConfig(4))
				printColor("Coming in v0.02.",getConfig(2))
				lineBreak(columns, getConfig(4))
				printColor("What is the name of the note you wish to edit?",getConfig(2),"")
				contentName = input(": ")
				while contentName == "":
					printColor("The note name cannot be empty. Please input a valid name.", getConfig(2))
					contentName = input(": ")

				search_response = apiCalls.searchNotes('title', contentName, ['content'])
				note_content = translation(search_response.content)
				newContent = input_pre_filled("Edit the note", note_content)
				apiCalls.addContent(contentName, newContent)
				lineBreak(columns, getConfig(4))
				printColor("Edits saved",getConfig(2))

				time.sleep(2)
				clearConsole()
				printAppUse()
				state = 1

		#addTag
			case 123:
				lineBreak(columns, getConfig(4))
				printColor("Adding tag...",getConfig(2),"")
				lineBreak(columns, getConfig(4))
				printColor("What is the name of the note you wish to add a tag to?",getConfig(2),"")
				addTagName = ""
				while addTagName == "":
					printColor("The note to add to cannot be empty. Please input a name.", getConfig(2))
					addTagName = input(": ")

				printColor("What is the tags that you wish to add? (List with commas and a space inbetween)", getConfig(2),"")
				addTags = input(": ")
				while addTags != 'none' and not all(tag.strip() for tag in newTags.split(',')):
					printColor("Tags should be separated by commas and a space. Please enter tags in the correct format.", getConfig(2))
					addTags = input(": ")
				tagsList = addTags.split(", ")
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
				while delTagName == "":
					printColor("The note to remove a tag from to cannot be empty. Please input a name.", getConfig(2))
					addTagName = input(": ")
				printColor("What is the tags that you wish to delete? (List with commas and a space inbetween)", getConfig(2),"")
				delTags = input(": ")
				while addTags != 'none' and not all(tag.strip() for tag in newTags.split(',')):
					printColor("Tags should be separated by commas and a space. Please enter tags in the correct format.", getConfig(2))
					delTags= input(": ")
				delTagsList = delTags.split(", ")
				apiCalls.deletetag(delTagName,delTagsList)
				lineBreak(columns, getConfig(4))
				printColor("Deleted tag(s)!",getConfig(2))
				time.sleep(2)
				clearConsole()
				printAppUse()	
				state = 1

		#addImage
			case 125:
				lineBreak(columns, getConfig(4))
				printColor("Adding image...",getConfig(2),"")
				lineBreak(columns, getConfig(4))
				printColor("What is the name of the note you wish to edit?",getConfig(2),"")
				noteTitle = input(": ")
				while noteTitle == "":
					printColor("The note to add an image to cannot be empty. Please input a name.", getConfig(2))
				printColor("What are the paths to the images you would like to attach? (List with commas between)", getConfig(2),"")
				imagePathInput = input(": ")
				imagePaths = imagePathInput.split(",")
				apiCalls.addImage(noteTitle, imagePaths)
				lineBreak(columns, getConfig(4))
				printColor("Added image(s)!", getConfig(2))
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
				printColor("1. View content", getConfig(2),"")
				printColor("2. By title", getConfig(2),"") 
				printColor("3. By created date",getConfig(2),"") 
				printColor("4. By modified date",getConfig(2),"")
				printColor("5. By tag",getConfig(2)) 

			case 1310 | 1320 | 1330 | 1340 | 1350:
				printAppUse()
				state = 1

		#view_content
			case 131:
				pass
				lineBreak(columns, getConfig(4))
				printColor("Enter title that you wish to view content of.",getConfig(2))
				lineBreak(columns, getConfig(4))
				search_by = input(": ")
				while search_by == "":
					printColor("The note to search for to cannot be empty. Please input a name.", getConfig(2))
					search_by = input(": ")
				desired_response = ['title','content']
				api_response = apiCalls.searchNotes('title', search_by, desired_response)
				entries = translation(api_response.content)
				parsing = entries.split("\n")
				test_split = parsing[1].replace(r'\n','\n')
				repeats = len(test_split)
				x=1
				printColor("File Name: ", getConfig(2))
				print("   " + parsing[x-1])
				printColor("Content: ", getConfig(2))
				print("   " + test_split)

		#title
			case 132:
				lineBreak(columns, getConfig(4))
				printColor("Enter title to search.",getConfig(2))
				lineBreak(columns, getConfig(4))
				search_by = input(": ")
				while search_by == "":
					printColor("The note to search for cannot be empty. Please input a name.", getConfig(2))
					search_by = input(": ")
				desired_response = ['title','modified_date','created_date']
				api_response = apiCalls.searchNotes('title', search_by, desired_response)
				entries = translation(api_response.content)
				parsing = entries.split("\n")
				repeats = len(parsing)
				x = 1
				while x < repeats:
					printColor("File Name: ", getConfig(2))
					print("   " + parsing[x-1])
					printColor("Created Date: ", getConfig(2))
					print("   " + parsing[x])
					printColor("Modified Date: ", getConfig(2))
					print("   " + parsing[x+1])
					print("\n")
					x = x+3
				
		#created_date
			case 133: #Currently not working
				lineBreak(columns, getConfig(4))
				printColor("Enter the beginning of the date range to search by.",getConfig(2))
				lineBreak(columns, getConfig(4))
				start = input(": ")
				while start == "":
					printColor("The date range to search by cannot be empty. Please input a date.", getConfig(2))
					start = input(": ")
				lineBreak(columns, getConfig(4))
				printColor("Enter the end of the date range to search by.",getConfig(2))
				lineBreak(columns, getConfig(4))
				end = input(": ")
				while end == "":
					printColor("The date range to search by cannot be empty. Please input a date.", getConfig(2))
					end = input(": ")
				desired_response = ['title','modified_date','created_date']
				api_response = apiCalls.searchNotes('created_date', "", desired_response, start, end)
				entries = translation(api_response.content)
				parsing = entries.split("\n")
				repeats = len(parsing)
				x = 1
				while x < repeats:
					printColor("File Name: ", getConfig(2))
					print("   " + parsing[x-1])
					printColor("Created Date: ", getConfig(2))
					print("   " + parsing[x])
					printColor("Modified Date: ", getConfig(2))
					print("   " + parsing[x+1])
					print("\n")
					x = x+3

		#modified_date
			case 134: #Currently not working
				lineBreak(columns, getConfig(4))
				printColor("Enter the beginning of the date range to search by.",getConfig(2))
				lineBreak(columns, getConfig(4))
				start = input(": ")
				while start == "":
					printColor("The date range to search by cannot be empty. Please input a date.", getConfig(2))
					start = input(": ")
				lineBreak(columns, getConfig(4))
				printColor("Enter the end of the date range to search by.",getConfig(2))
				lineBreak(columns, getConfig(4))
				end = input(": ")
				while end == "":
					printColor("The date range to search by cannot be empty. Please input a date.", getConfig(2))
					end = input(": ")
				desired_response = ['title','modified_date','created_date']
				api_response = apiCalls.searchNotes('modified_date', "", desired_response, start, end)
				entries = translation(api_response.content)
				parsing = entries.split('\n')
				repeats = len(parsing)
				x = 1
				while x < repeats:
					printColor("File Name: ", getConfig(2))
					print("   " + parsing[x-1])
					printColor("Created Date: ", getConfig(2))
					print("   " + parsing[x])
					printColor("Modified Date: ", getConfig(2))
					print("   " + parsing[x+1])
					print("\n")
					x = x+3

        #search by tag
			case 135: 
				lineBreak(columns, getConfig(4))
				printColor("Enter tag to search.", getConfig(2))
				lineBreak(columns, getConfig(4))
				search_by = input(": ")
				while search_by == "":
					printColor("The tag to search for cannot be empty. Please input a tag name.", getConfig(2))
					search_by = input(": ")
				desired_response = ['title', 'tag']
				api_response = apiCalls.searchNotesByTag(search_by, desired_response)
				entries = translation(api_response.content)
				parsing = entries.split('\n')
				repeats = len(parsing)
				x = 1
				#y = 1
				while x < repeats:
					printColor("File Name: ", getConfig(2))
					print("   " + parsing[x-1])
					printColor("Note Tag: ", getConfig(2))
					print("   " + parsing[x])
					print("\n")
					x = x+2

		#listNotes
			case 14:
				lineBreak(columns, getConfig(4))
				printColor("Listing notes...",getConfig(2))
				lineBreak(columns, getConfig(4))
				printColor("0. Go back",getConfig(2),"")
				printColor("1. By title",getConfig(2),"")
				printColor("2. By created date",getConfig(2),"")
				printColor("3. By modified date",getConfig(2),"")
				printColor("4. List Tags", getConfig(2))


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
				parsing = entries.split('\n')
				repeats = len(parsing)
				x = 1
				while x < repeats:
					printColor("File Name: ", getConfig(2))
					print("   " + parsing[x-1])
					x = x+1

				

		#list notes by created date
			case 142:
				lineBreak(columns, getConfig(4))
				printColor("Listing notes by created date...",getConfig(2))
				lineBreak(columns, getConfig(4))
				gotList = apiCalls.listNotes("created_date")
				
				#printing the response
				entries = translation(gotList.content)
				parsing = entries.split('\n')
				repeats = len(parsing)
				x = 1
				while x < repeats:
					printColor("File Name: \n", getConfig(2),"")
					print("   " + parsing[x-1])
					printColor("Created Date: ", getConfig(2))
					print("   " + parsing[x])
					x = x+2

				

		#list notes by modified date
			case 143:
				lineBreak(columns, getConfig(4))
				printColor("Listing notes by modified date...",getConfig(2))
				lineBreak(columns, getConfig(4))
				gotList = apiCalls.listNotes("modified_date")

				#printing the response
				entries = translation(gotList.content)
				parsing = entries.split('\n')
				repeats = len(parsing)
				x = 1
				while x < repeats:
					printColor("File Name: \n", getConfig(2),"")
					print("   " + parsing[x-1])
					printColor("Modified Date: ", getConfig(2))
					print("   " + parsing[x])
					x = x+2


    
        #list all tags
			case 144: #Currently not working
				tags = apiCalls.listTags()
				print(tags)
				#printColor("Tags:\n" + "\n".join([f"{tag['title']}: {tag['tag']}" for tag in tags]), getConfig(2))
				time.sleep(2)
				state = 1   
        
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
        
		#Tag menu stuff
			case 16: #Unsure if tag menu stuff is working as search and list is not working.
				printTagMenu()

			case 1640:
				printAppUse()
				state = 1

			case 161:
				lineBreak(columns, getConfig(4))
				printColor("Adding tag...",getConfig(2),"")
				lineBreak(columns, getConfig(4))
				printColor("What is the name of the note you wish to edit?",getConfig(2),"")
				addTagName = input(": ")
				while addTagName == "":
					printColor("The note to search for cannot be empty. Please input a note name.", getConfig(2))
					addTagName = input(": ")
				printColor("What is the tags that you wish to add? (List with commas and a space inbetween)", getConfig(2),"")
				addTags = input(": ")
				while addTags != 'none' and not all(tag.strip() for tag in newTags.split(',')):
					printColor("Tags should be separated by commas and a space. Please enter tags in the correct format.", getConfig(2))
					addTags = input(": ")
				tagsList = addTags.split(", ")
				apiCalls.addTag(addTagName,tagsList)
				lineBreak(columns, getConfig(4))
				printColor("Added tag(s)!", getConfig(2))
				time.sleep(2)
				clearConsole()
				printAppUse()
				state = 1

			case 162:
				lineBreak(columns, getConfig(4))
				printColor("Deleting tag...",getConfig(2),"")
				lineBreak(columns, getConfig(4))
				printColor("What is the name of the note you wish to edit?",getConfig(2),"")
				delTagName = input(": ")
				while delTagName == "":
					printColor("The tag to search for cannot be empty. Please input a tag name.", getConfig(2))
					delTagName = input(": ")
				printColor("What is the tags that you wish to delete? (List with commas and a space inbetween)", getConfig(2),"")
				delTags = input(": ")
				while delTags != 'none' and not all(tag.strip() for tag in newTags.split(',')):
					printColor("Tags should be separated by commas and a space. Please enter tags in the correct format.", getConfig(2))
					delTags = input(": ")
				delTagsList = delTags.split(", ")
				print(delTagsList[1])
				apiCalls.deletetag(delTagName,delTagsList)
				lineBreak(columns, getConfig(4))
				printColor("Deleted tag(s)!",getConfig(2))
				time.sleep(2)
				clearConsole()
				printAppUse()	
				state = 1
			
			case 163:
				tags = apiCalls.listTags()
				#printColor("Tags:\n" + "\n".join([f"{tag['title']}: {tag['tag']}" for tag in tags]), getConfig(2))
				time.sleep(2)
				state = 1

			case 164:
				lineBreak(columns, getConfig(4))
				printColor("Enter tag to search.", getConfig(2))
				lineBreak(columns, getConfig(4))
				search_by = input(": ")
				while search_by == "":
					printColor("The tag to search by cannot be empty. Please input a tag name.", getConfig(2))
					search_by = input(": ")
				desired_response = ['title', 'tag']
				api_response = apiCalls.searchNotesByTag(search_by, desired_response)
				entries = translation(api_response.content)
				parsing = entries.split('\n')
				repeats = len(parsing)
				x = 1
				#y = 1
				while x < repeats:
					printColor("File Name: ", getConfig(2))
					print("   " + parsing[x-1])
					printColor("Note Tag: ", getConfig(2))
					print("   " + parsing[x])
					print("\n")
					x = x+2

			case 165:
				printColor("Renaming a tag...", getConfig(2))
				lineBreak(columns, getConfig(4))
				printColor("Enter the current tag name:", getConfig(2))
				old_tag = input(": ")
				while old_tag == "":
					printColor("The tag to rename cannot be empty. Please input a tag name.", getConfig(2))
					old_tag = input(": ")
				printColor("Enter the new tag name:", getConfig(2))
				new_tag = input(": ")
				while new_tag == "":
					printColor("The new name cannot be empty. Please input a tag name.", getConfig(2))
					new_tag = input(": ")
				apiCalls.renameTag(old_tag, new_tag)
				lineBreak(columns, getConfig(4))
				printColor("Tag renamed successfully!", getConfig(2))
				time.sleep(2)
				clearConsole()
				printAppUse()
				state = 1

          
    	# Convert Notes To MKDown
			case 17: #Unsure if working, can writer please tell me if working
				lineBreak(columns, getConfig(4))
				printColor("What is the title of the note you would like to convert to MKDown?",getConfig(2), "")
				lineBreak(columns,getConfig(4))
				search_by = input(": ")
				while search_by == "":
					printColor("The note to search for cannot be empty. Please input a note name.", getConfig(2))
					search_by = input(": ")
				desired_response = ['content']
				api_response = apiCalls.searchNotes('title', search_by, desired_response)
				entries = translation(api_response.content)
				parsing = entries.split("\n")
				content = parsing[1].replace(r'\n', '\n')
				title = parsing[0]
				if ".md" not in title: 
					title = title + ".md"
				apiCalls.mdDownConversion(title, content)
				printColor("Note converted successfully!", getConfig(2))
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
				while response != 1 and response != 0:
					printColor("Please enter a number")
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
				while int(newColor) not in range(1,256):
					printColor("Please enter a number")
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
				while int(newColor) not in range(1,256):
					printColor("Please enter a number", getConfig(2))
					newColor = input(": ")
				setConfig(4,newColor)
				clearConsole()
				lineBreak(columns, getConfig(4))
				printColor("Success, enter 0 to go back", getConfig(2))
				lineBreak(columns, getConfig(4))
            
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
				while True:
					if userInput.isdigit():
						userInputFixed = int(userInput)
						if 0 <= userInputFixed <= 9:
							state = (state * 10) + userInputFixed
							break
						else:
							printColor("Invalid input. Please enter a number between 0 and 9.", getConfig(2))
							userInput = input(": ")
					else:
						printColor("Invalid input. Please enter a number between 0 and 9.", getConfig(2))
						userInput = input(": ")

         
# Runtime
runtime(0)

