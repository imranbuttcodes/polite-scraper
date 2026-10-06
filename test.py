from bs4 import BeautifulSoup

html = """
<html>
    <body>
        <h1>Hello BeautifulSoup</h1>
        <p>This is my first scraper.</p>
        <p>This is my Second scraper.</p>
    </body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")
h1 = soup.find("h1")
print("BRO:",type(h1.text))
p = soup.find("p")
print("BRO:",p)
b = soup.find("body")
print("BRO:",b)