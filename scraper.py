import requests
import time
from bs4 import BeautifulSoup

# 1. Introduce ourselves politely
HEADERS = {
    "User-Agent": "PoliteScraper/1.0 (Learning Project; imranbutteng@gmail.com)"
}

def download_page(url: str):
    print(f"Politely requesting: {url}...")
    
    # 2. Pause for 1 second before knocking on the door
    time.sleep(1)
    
    # 3. Request the page using our custom headers
    response = requests.get(url, headers=HEADERS)
    
    # 4. If the server says "404 Not Found", this will immediately raise an error
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
    for book in books[:3]:
        # Extract the title (it's inside an <h3> tag, inside an <a> tag)
        title = book.h3.a["title"]
        
        # Extract the price (it's inside a <p class="price_color"> tag)
        price_text = book.find("p", class_="price_color").text
        
        # Extract availability
        availability = book.find("p", class_="instock availability").text.strip()
        
        print(f"Title: {title}")
        print(f"Price: {price_text}")
        print(f"Availability: {availability}")
        print("-" * 30)
