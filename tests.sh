#!/bin/bash

# script for running automatic tests with curl
# run these lines in a different terminal before running this
# rm note.db
# flask run

today=$(date '+%Y-%m-%d')
# create notes
 curl -H 'Content-Type: application/json' \
      -d '{"title":"my note"}' \
      -X POST \
      http://127.0.0.1:5000/notes

curl -H 'Content-Type: application/json' \
      -d '{"title": "your note",
			"content": "Today in class we will..."}' \
      -X POST \
      http://127.0.0.1:5000/notes

# tags create
curl -H 'Content-Type: application/json' \
      -d '{"title": "your note",
		"tag": ["fun"]}' \
      -X POST \
      http://127.0.0.1:5000/tags
curl -H 'Content-Type: application/json' \
      -d '{"title": "my note",
		"tag": ["boring", "fun"]}' \
      -X POST \
      http://127.0.0.1:5000/tags

# notes search
# return content and search by title
curl -H 'Content-Type: application/json' \
      -d '{"search_field":"title",
    	"query":"your note",
    	"return_fields":["content"]}' \
      -X GET \
      http://127.0.0.1:5000/notes/search
# return created date and search by created date
curl -H 'Content-Type: application/json' \
      -d '{"search_field":"created_date",
    	"query":"'"$today"'",
    	"return_fields":["created_date"]}' \
      -X GET \
      http://127.0.0.1:5000/notes/search
# return modified date and title search by modified date
curl -H 'Content-Type: application/json' \
      -d '{"search_field":"modified_date",
    	"query":"'"$today"'",
    	"return_fields":["modified_date", "title"]}' \
      -X GET \
      http://127.0.0.1:5000/notes/search
# tag list
curl -H 'Content-Type: application/json' \
      -d '{}' \
      -X GET \
      http://127.0.0.1:5000/tags/list
# tags search
# >1 match
curl -H 'Content-Type: application/json' \
      -d '{"query": "boring"}' \
      -X GET \
      http://127.0.0.1:5000/tags/search
# ==1 match
curl -H 'Content-Type: application/json' \
      -d '{"query": "fun"}' \
      -X GET \
      http://127.0.0.1:5000/tags/search