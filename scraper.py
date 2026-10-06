import requests
import time
from bs4 import BeautifulSoup
from pydantic import BaseModel, field_validator


# 1. Introduce ourselves politely
HEADERS = {
    "User-Agent": "PoliteScraper/1.0 (Learning Project; imranbutteng@gmail.com)"
}


# --- Data Schema ---
class Book(BaseModel):
    title: str
    price: float  # We want a real number, NOT a string with a £ sign!
    availability: str

    # This validator runs automatically every time a Book is created
    @field_validator("price", mode="before")
    def clean_price(cls, value):
        if isinstance(value, str):
            # Strip out the '£' symbol and turn the rest into a float
            cleaned_string = value.replace("£", "").strip()
            return float(cleaned_string)
        return value


def download_page(url: str):
    print(f"Politely requesting: {url}...")
    
    # Pause for 1 second before knocking on the door
    time.sleep(1)
    
    # Request the page using our custom headers
    response = requests.get(url, headers=HEADERS)
    
    response.encoding = "utf-8"
    
    # If the server says "404 Not Found", this will immediately raise an error
    response.raise_for_status() 
    
    return response.text

# --- Let's test it! ---
if __name__ == "__main__":
    test_url = "https://books.toscrape.com/catalogue/page-1.html"
    html_content = download_page(test_url)
    
    print("Parsing HTML...")
    # 1. Hand the messy HTML over to BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 2. Find all the "book boxes" on the page
    # (On this website, every book is wrapped in an <article class="product_pod"> tag)
    books = soup.find_all("article", class_="product_pod")
    
    print(f"Found {len(books)} books on the page!\n")

    # 3. Let's loop through just the first 3 books to see what data we can grab
        # 3. Let's loop through just the first 3 books
    for book in books[:3]:
        title = book.h3.a["title"]
        price_text = book.find("p", class_="price_color").text
        availability = book.find("p", class_="instock availability").text.strip()
        
        # --- Pass the messy data into our strict Pydantic model ---
        clean_book = Book(
            title=title,
            price=price_text,
            availability=availability
        )
        
        # Notice how the price prints out as a clean number now!
        print(clean_book.model_dump())
        