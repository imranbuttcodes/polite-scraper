# Polite E-Commerce Scraper 🤖

A robust, polite Python web scraper built to extract, clean, and validate book data from `books.toscrape.com`.

## Features
- **Polite Execution:** Uses custom `User-Agent` headers and implements a 1-second delay between requests to respect server loads.
- **Robust Parsing:** Uses `BeautifulSoup4` to cleanly extract messy HTML.
- **Strict Data Validation:** Leverages `Pydantic V2` schemas to automatically strip currency symbols (`£`), fix encoding artifacts (`Â`), and strictly type-cast prices to `float`.
- **Fault Tolerant:** Implements error handling to gracefully survive `404 Not Found` pages without crashing.
- **JSON Export:** Dumps all clean, structured data into `books.json`.

## How to Run

1. **Activate your virtual environment** (if not already active):
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the scraper:**
   ```bash
   python scraper.py
   ```
   *The scraper will output its progress to the terminal and generate a clean `books.json` file in the root directory.*
