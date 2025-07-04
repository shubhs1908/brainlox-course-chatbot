from langchain_community.document_loaders import WebBaseLoader
from bs4 import BeautifulSoup
import json
import os

# Set User-Agent (Pretend to be a normal browser)
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Load website content
url = "https://brainlox.com/courses/category/technical"
loader = WebBaseLoader(url)
docs = loader.load()

# Extract text from HTML
def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

# Store extracted data
data = [{"content": clean_html(doc.page_content), "source": doc.metadata["source"]} for doc in docs]

# Save data as JSON
with open("brainlox_courses.json", "w") as f:
    json.dump(data, f, indent=4)

print("Data Scraped and Saved!")