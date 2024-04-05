import os
import shutil
import string

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
	printColor("1. Open app        2. Settings        3. Help", getConfig(2))

def optionColors():
	for i in range(0,255):
		print(f"\033[38;5;{str(i)}m{i}\033[0m", end = ", ")

def printAppUse():
	columns = shutil.get_terminal_size()[0]
	lineBreak(columns, getConfig(4))
	printColor("1. New Note        2. Edit Note        3. Search Notes        4. List Notes        5. Delete Note", getConfig(2))
	lineBreak(columns, getConfig(4))
	printColor("To exit, enter '0'.", getConfig(2))
	pass


def printSettings():
	columns = shutil.get_terminal_size()[0]
	lineBreak(columns, getConfig(4))
	printColor("Settings", getConfig(2), "\n")
	printColor("1. Pro mode: " + getConfig(6), getConfig(2), "")
	printColor("2. Change Primary Color (WARNING: Opens a menu)", getConfig(2))
	printColor("3. Change Secondary Color (WARNING: Opens a menu)", getConfig(2))
	lineBreak(columns, getConfig(4))
	printColor("To edit, enter the number of the feature you wish to edit.", getConfig(2),"")
	printColor("To exit, enter '0'.", getConfig(2))

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
	printColor("To exit, enter '0'.", getConfig(2))

# testblock
printStartScreen()
printSettings()
printHelpScreen()
printAppUse()
setConfig(2, 2)