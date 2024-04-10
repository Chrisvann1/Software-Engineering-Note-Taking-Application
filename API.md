# Specs for the API requests
This document identifies the current design of the API backend.
It should serve as a reference for API callers.
Please do not take the syntax seriously. You may need to implement these calls differently.
This is a skeletal structure outlining what the API is capable of.

## Feature 1: Create a note
Creates a note that does not exist. Raises an error if a note with that title already exists.

```
POST /notes
```
header:
	`Content-Type: application/json` (required)
body:
	`'title'` (required): string of note title
    `'content'` (optional): string of note content
response:
	None
## Feature 2: Delete a note
Deletes a note. It will no longer show up in the tags or the notes table.
```
DELETE /notes
```
header:
	`Content-Type: application/json` (required)
body:
	`'title'` (required): string of note title
response:
	None
## Feature 3: Edit a note
Changes the content of a note.
```
PUT /notes
```
header:
	`Content-Type: application/json` (required)
body:
	`'title'` (required): string of note title
	`'content'` (required): string of note's new content
response:
	None
## Feature 4: List notes
This is an interesting feature which seems vague and confusing. We implement it like this.
We interpret the `specs.md` file to mean that this feature should list all of the notes.
Our version lists the title values and 'list_field' values of all of the notes
```
GET /notes/list
```
header:
	`Content-Type: application/json` (required)
body:
	`'list_field'` (optional): string representing note field to list by. always lists by at least title.
		- must be in ('modified_date', 'title', 'created_date', 'content')
## Additional Feature 1: Search notes by note content
We don't currently support search by note content!
We aren't be able to run this with `'search_field': 'content'`
```
GET /notes/search
```
header:
	`Content-Type: application/json` (required)
body:
	`'search_field'` (required): string representing note field to search by.
		- must be in ('modified_date', 'title', 'created_date', 'tag')
	`'query'` (required): string representing the string to search for in the 'search_field'
	`'return_fields'` (required): list of strings representing aspects of the notes you want returned back to you
		- must be in ('modified_date', 'title', 'created_date', 'tag')

## Additional Feature 2: Search by title
Run this with `'search_field': 'title'`
```
GET /notes/search
```
header:
	`Content-Type: application/json` (required)
body:
	`'search_field'` (required): string representing note field to search by.
		- must be in ('modified_date', 'title', 'created_date', 'tag')
	`'query'` (required): string representing the string to search for in the 'search_field'
	`'return_fields'` (required): list of strings representing aspects of the notes you want returned back to you
		- must be in ('modified_date', 'title', 'created_date', 'tag')

## Additional Feature 3: Create a directory/tag
Creates a list of tags to be applied to a specific note.
```
POST /tags
```
header:
	`Content-Type: application/json` (required)
body:
	`'title'` (required): string representing specific note title.
	`'tag'` (required): List of strings representing the names of the tags you want to apply'
		example format: ["Tag title 1", "Tag title 2", "TAG title three"]
## Additional Feature 4: Delete a directory/tag

## Additional Feature 5: List directories/tags

