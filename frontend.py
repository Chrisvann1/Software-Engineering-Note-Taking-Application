import os
import shutil
import string
import time

import apiCalls

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
	printColor("5. Delete Note",getConfig(2),"")
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

			case 11:
				#newNote
				lineBreak(columns, getConfig(4))
				printColor("Creating note...", getConfig(2))
				lineBreak(columns, getConfig(4))
				printColor("What would you like to name your new note?",getConfig(2), "")
				newNoteName = input(": ")
				printColor("What content would you like to add to start? (If you wish to add content later, enter 'none'.)", getConfig(2),"")
				newContent = input(": ")
				if (newContent == 'none'):
					pass
					#apiCalls.createNote(newNoteName,"")
				else:
					pass
					#apiCalls.createNote(newNoteName,newContent)
				printColor("Would you like to add any tags? (Seperate tags with commas. If none or you wish to add later, enter 'none'.)",getConfig(2),"")
				newTags = input(": ")
				newTagList = newTags.split(",")
				if(newTags == 'none'):
					lineBreak(columns, getConfig(4))
					printColor("Note Created!",getConfig(2))
					time.sleep(3)
					printAppUse()
					state = 1
				else:
					#apiCalls.addTag(newNoteName,newTagList)
					lineBreak(columns,getConfig(4))
					printColor("Note Created!", getConfig(2))
					time.sleep(3)
					printAppUse()
					state = 1
				
				
			case 12:
				#editNote
				pass
			case 121:
				#addContent
				pass
			case 122:
				#editContent (limited/cut temporarily from time)
				pass
			case 123:
				#addTag
				pass
			case 124:
				#deleteTag
				pass

			case 13:
				#searchNotes
				pass

			case 14:
				#listNotes
				pass
			case 141:
				#list notes by created date
				pass
			case 142:
				#list notes by modified date
				pass
			case 143:
				#list notes by title
				pass
			case 144:
				#list tags
				pass

			case 15:
				#deleteNote
				lineBreak(columns, getConfig(4))
				printColor("Deleting note...", getConfig(2))
				lineBreak(columns, getConfig(4))
				printColor("Enter the name of the note you wish to delete.",getConfig(2),"")
				delNoteName = input(": ")
				#apiCalls.deleteNote(delNoteName)
				printColor("Note deleted or it already does not exist", getConfig(2))
				time.sleep(3)
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