import os
import shutil
import string

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



# Http integration managment
# generic verion of a http request, formats to request well.
def request():
	pass

# generic version of a http response, formats to respond well.
def response():
	pass



# Note Searching
def listNotes():
	#by created date, modified date, title
	pass

def searchNotes():
	#by content, title, tags, date
	pass



# Note Classification Suite
def addTag():
	# Makes a list of tags that should be added to the title, does not need to check if tags exist
	pass

def deletetag():
	# Delete a tag from a note
	pass

def listTags():
	# Lists tags of all notes
	pass 



# Note creation suite
def createNote():
	#addTag()
	pass 

def deleteNote():
	pass

def addContent():
	# This should add to an existing note
	pass 



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
	printColor("1. New Note        2. Edit Note        3. Search Notes        4. List Notes        5. Delete Note", getConfig(2))
	lineBreak(columns, getConfig(4))
	printColor("To continue, enter the number of what you wish to do.",15)
	printColor("To exit, enter '0'.", 15)
	pass

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

			# General Help page	
			case 3:
				printHelpScreen() 
			case 999:
				printColor("Invalid state", 9)
				break
		userInput = input(": ")
		# temporary
		if (state == 0 and userInput == '0'):
			state = -1
		else:
			state = (state * 10) + int(userInput)



# testblock
runtime(0)