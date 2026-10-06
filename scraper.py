import requests
import time
from bs4 import BeautifulSoup
from pydantic import BaseModel, field_validator
import json


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


if __name__ == "__main__":
    all_clean_books = []
    
    # We want to scrape Pages 1, 2, and 3
    # We will also try Page 999 just to prove our script survives a broken page!
    pages_to_scrape = [1, 2, 3, 999]
    
    for page_num in pages_to_scrape:
        url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"
        
        try:
            html_content = download_page(url)
            soup = BeautifulSoup(html_content, "html.parser")
            books = soup.find_all("article", class_="product_pod")
            
            for book in books:
                title = book.h3.a["title"]
                price_text = book.find("p", class_="price_color").text
                availability = book.find("p", class_="instock availability").text.strip()
                
                # Clean and validate!
                clean_book = Book(title=title, price=price_text, availability=availability)
                
                # Save the clean python dictionary to our master list
                all_clean_books.append(clean_book.model_dump())
                
        except requests.exceptions.HTTPError as e:
            # If the page doesn't exist (like page 999), the server returns a 404 error.
            # Instead of crashing, we catch it gracefully!
            print(f"⚠️ Whoops! Page {page_num} is broken or doesn't exist. Skipping it!")
            continue

    # Finally, save all 60 books to a JSON file!
    print(f"\nSuccessfully scraped {len(all_clean_books)} books!")
    
    with open("books.json", "w") as f:
        json.dump(all_clean_books, f, indent=4)
        
    print("Saved all data to books.json!")
