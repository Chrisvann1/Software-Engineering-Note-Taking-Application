import os
import shutil
import string

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

def printColor(text, color, tail = "\n"):
	color = str(color)
	print(f"\033[38;5;{color}m{text}\033[0m", end = tail)

def lineBreak(columns, color):
	line = '-'
	for i in range(1,columns):
		line += '-'
	printColor(line, color, "")

def printStartScreen():
	columns = shutil.get_terminal_size()[0]
	lineBreak(columns, getConfig(4))
	printColor("Welcome to appName, select what you want to do", getConfig(2), "")
	lineBreak(columns, getConfig(4))
	print("\n")
	printColor("1. Open app        2. Settings        3. Help", 15)

def optionColors():
	for i in range(0,255):
		print(f"\033[38;5;{str(i)}m{i}\033[0m", end = ", ")

def printSettings():
	columns = shutil.get_terminal_size()[0]
	lineBreak(columns, getConfig(4))
	printColor("Settings", getConfig(2), "")
	lineBreak(columns, getConfig(4))

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
			case 20 | 30:
				printStartScreen()
				state = 0
			# Application-in-use page
			#case 1:

			# Settings page
			case 2:
				printSettings()
			case 220 | 230:
				printSettings()
				state = 2
			# Primary color selection
			case 22:
				lineBreak(columns, 15)
				print("Choose a primary color")
				printColor("current color", getConfig(2))
				lineBreak(columns, 15)
				optionColors()
				newColor = input(": ")
				setConfig(2,newColor)
			# Secondary color selection
			case 23:
				lineBreak(columns, 15)
				print("Choose a secondary color")
				printColor("current color", getConfig(4))
				lineBreak(columns, 15)
				optionColors()
				newColor = input(": ")
				setConfig(4,newColor)
			# General Help page	
			case 3:
				pass 
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