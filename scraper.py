import requests
import time

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
    
    print(f"Success! Downloaded {len(html_content)} characters of HTML data.")
