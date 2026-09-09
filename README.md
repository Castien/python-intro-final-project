# Open Library Book Search

A command-line program that uses the Open Library API to search for books by author. The program displays information about each matching book, including its title, author, publication year, edition count, and available languages.

# API

This project uses the [Open Library Search API](https://openlibrary.org/developers/api).

The program uses the search endpoint:

`https://openlibrary.org/search.json`

The author's name is passed as a query parameter.

# Installation

1. Clone this repository:

   ```bash
   git clone git@github.com:Castien/python-intro-final-project.git
   cd python-intro-final-project
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   On macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

   On Windows:

   ```bash
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

# Usage

Run the program from the project directory:

```bash
python main.py
```

The program prompts the user to enter an author's name. The program sends the author name to the Open Library API and displays information about the books returned by the search.

If no author is entered, the program asks the user to enter an author's name. API connection errors are handled without crashing the program.

# CLI Interactions

* **Search by author** — enter an author's name to see a list of books associated with that author.
* **Empty input** — if no author is entered, the program displays a message asking the user to provide an author's name.
