import os
import shutil

def lineBreak(columns):
	line = '-'
	for i in range(1,columns):
		line += '-'
	print(line)

def printStartScreen():
	columns = shutil.get_terminal_size()[0]
	lineBreak(columns)
	print("Welcome to appName, select what you want to do")
	lineBreak(columns)
	print("1. Open app        2. Settings        3. Help")

#def printOtherthing():

# testblock
printStartScreen();