
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
# number_of_pages_median
# subject (list)

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

# Replace with your chosen API endpoint
API_URL = "https://openlibrary.org/search.json"  

# Fetch Data:
# User input for record search.
# Send request to Open Library.
# Get JSON response.
# Return raw data.
# Handle network/API exceptions with try/except.
    
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

# Testing
# data = fetch_data("J.R.R. Tolkien")
# print(data["docs"][0])

# data = fetch_data("J.R.R. Tolkien")
# books = process_data(data)
# print(books)

def display_results(results):
    """Print results to the terminal in a readable format."""
    for book in results:
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Year: {book['year']}")
        print(f"Editions: {book['editions']}")
        print(f"Languages: {book['languages']}")
        print()

def main():
    author = input("Enter an author's name: ")
    data = fetch_data(author)
    if not data:
        return

    records = process_data(data)

    display_results(records)


if __name__ == "__main__":
    main()