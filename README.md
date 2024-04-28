# Software-Engineering-Note-Taking-Application

# Noteworthy II: a command line-based note taking application

## Welcome!

Noteworthy is an application that will store notes in a searchable and listable database, allowing you to create, tag, search, and organize your notes in a lightweight command line environment.

## What you'll need

Noteworthy requires Python version 3.10 or later, and uses the following [extensions]:

* string
* requests
* easygui
* flask
* json
* datetime

## How to Use

### Installation

First, download all the project files and store them in a directory of your choice. You will run two Python files: frontend.py, which runs the menus and user inputs, and app.py, which runs the API and puts your inputs into the database. In the future (not really, lol) we will make the API run seperately so users only have to run one file, but for now you'll have to run them both locally.

### Navigation

Each of the menus will give you a list of several numbered options. Enter the number of your desired selection in the command line and hit Enter, and your choice will be selected. '0' always means Go Back, so if you've entered a menu or function and want to get out, input '0'.

### Troubleshooting

If the program becomes stuck or you just need to abort and reset it, type CTRL-C; this will forcibly exit the program. If you find an issue or bug, check the project's Github page and consider leaving your feedback if the issue hasn't already been addressed.