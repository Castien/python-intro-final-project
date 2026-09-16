
# 1. What is the URL you'll call? 
#    Write the exact endpoint, including any query parameters you plan to use.

# https://openlibrary.org/search.json
# The author will be the primary query parameter.
# Future expansion would probably use ISBN.

# 2. What is the shape of the response? Is the top-level response a list? 
#    A dict with a list inside it? If it's a dict, what key holds the records you care about?

# The top-level response is a dictionary under the "docs" key.
# 'docs' contains a list of dictionaries, each dictionary representing a book.

# 3. Which 3-5 fields will your program use? 
#    List the field names exactly as they appear in the JSON. 
#    Note if any are nested inside another dict.

# title
# author_name (list)
# first_publish_year
# edition_count
# language (list)

# 4. What can a user do with your CLI? 
#    Describe the one core interaction in one sentence. 
#    For example: "A user can type a region name and see all countries in that region."

# A user can enter an author's name and see a list of books.

# 5. Where could things go wrong? 
#    Name two things that could fail at runtime 
#    - a bad network connection, a missing field, unexpected user input 
#    - and where in your code you'd handle each one.

# Error: API request could fail and give a network error.
# Handled: Try/except in function that retrieves the data from the API.

# Error: A book may be missing information being called on. 
# Handled: .get() to avoid KeyErrors and fill with default data, ex. 'N/A'


import requests
import csv

# Replace with your chosen API endpoint
API_URL = "https://openlibrary.org/search.json"  
 
def fetch_data(author):
    """Fetch data from the API. Returns the raw JSON response, or an empty list on failure."""
    try:
        response = requests.get(API_URL, params={"author": author})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: could not fetch data. {e}")
        return []

def process_data(data):
    books = []
    for book in data.get("docs", []):
        book_data = {
            "title": book.get("title", "N/A"),
            "author": book.get("author_name", ["N/A"])[0],
            "year": book.get("first_publish_year", "N/A"),
            "editions": book.get("edition_count", "N/A"),
            "languages": book.get("language", ["N/A"])
        }
        books.append(book_data)
    return books

# title	: If missing, use the author name as the title
# author : If missing, use "Unknown"
# year : If missing or invalid, use 0
# editions : If missing or invalid, use 0
# languages : Leave out of the CSV (for now)

def clean_data(records):
    cleaned_records = []

    for book in records:
        title = book["title"]
        author = book["author"]
        year = book["year"]
        editions = book["editions"]

        if title == "N/A":
            title = author

        if author == "N/A":
            author = "Unknown"

        if year == "N/A":
            year = 0
        else:
            try:
                year = int(year)
            except ValueError:
                year = 0

        if editions == "N/A":
            editions = 0
        else:
            try:
                editions = int(editions)
            except ValueError:
                editions = 0

        cleaned_book = {
            "title": title,
            "author": author,
            "year": year,
            "editions": editions
        }

        cleaned_records.append(cleaned_book)

    return cleaned_records

def export_csv(records, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["title", "author", "year", "editions"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(records)

# def is_valid(book):
#     return book["title"] != "N/A"

def display_results(results):
    """Print results to the terminal in a readable format."""
    for book in results:
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Year: {book['year']}")
        print(f"Editions: {book['editions']}")
        # print(f"Languages: {book['languages']}")
        print()

def main():
    author = input("Enter an author's name: ")
    if not author:
        print("Please enter an author's name.")
        return

    data = fetch_data(author)
    if not data:
        print("No results found.")
        return

    records = process_data(data)
    cleaned_records = clean_data(records)

    display_results(cleaned_records)
    export_csv(cleaned_records, "books.csv")


if __name__ == "__main__":
    main()