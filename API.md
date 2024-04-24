# Specs for the API requests
This document identifies the current design of the API backend.
It should serve as a reference for API callers.
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
	see response section
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
	see response section
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
	see response section
## Dates: Formatting for dates

## Requests: A design for the request dictionary
The request dictionary keys required for a call to the backend depends on the endpoint you are calling. The keys are specified in this document under the "body" sections for the corresponding feature. For example, by reading the Feature 3 section you would know that the `PUT /notes` request JSON dictionary has the following format

```
{
	"title": "new note title",
	"content": "This is my new note content\nI love taking notes with this app :))"
}
```
Notice that the body sections in this documentation are specifying the keys for this request. 
## Responses: A design for response dictionary
For lists and search (GET) requests there are nested list responses. Those nested lists depend on the request you are sending and the endpoint you are sending it to.
```
[
	["object1_field1_value",
	"object1_field2_value",
	"object1_field3_value"],
	["object2_field1_value",
	"object2_field2_value",
	"object2_field3_value"],
	["object3_field1_value",
	"object3_field2_value",
	"object3_field3_value"]
	...
]
```
For /notes/search GET methods the specific fields 1, 2, 3 etc. to return are defined by the `result_fields` list in the request body.
If title is not provided as a `return_fields` value then it is automatically added at the end.

For /tags/search the specific fields are automatically title and tag in that order.

For /notes/list GET methods only one field other than title is allowed to be returned. That field is defined by the `list_field` value in the request body.

For /tags/list the specific fields are automatically title and tag in that order.

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
```
GET /notes/search
```
header:
	`Content-Type: application/json` (required)
body:
	`'search_field'` (required): string representing note field to search by.
		- must be in ('modified_date', 'title', 'created_date')
	`'query'` (required): string representing the string to search for in the 'search_field'
	`'return_fields'` (required): list of strings representing aspects of the notes you want returned back to you
		- must be in ('modified_date', 'title', 'created_date', 'tag')
	`'start'` (option): start date for range to search by date within
	`'end'` (option): end date for range to search by date within

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
	`"title"` (required): string of note title
	`"tag"` (required): list of strings for tags Exp: "tag":["tag1", "tag2", "tag3"]
## Additional Feature 4: Delete a directory/tag
```
DELETE /tags
```
header:
	`Content-Type: application/json` (required)
body:
	`"title"` (required): string of note title
	`"tag"` (required): list of strings for tags. Exp: "tag":["tag1", "tag2", "tag3"]
## Additional Feature 5: List directories/tags
List all the tags that exist.
```
GET /tags/list
```
header:
	`Content-Type: application/json` (required)
body:
	none required
response:
```
{
	"tags" : ["tag1", "tag2", "tag3"]
}
```

