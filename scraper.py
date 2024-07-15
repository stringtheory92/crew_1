import requests
from bs4 import BeautifulSoup
import sqlite3

def scrape_articles():
    url = 'https://news.google.com/search?q=artificial+intelligence&hl=en-US&gl=US&ceid=US:en'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Need to tweak for html structure
    articles = []
    for item in soup.find_all('article'):  
        title_tag = item.find('h3')
        if title_tag:
            title = title_tag.text
            link = title_tag.find('a')['href']
            link = f"https://news.google.com{link[1:]}"  
            summary = item.find('p').text if item.find('p') else 'No summary available'
            articles.append((title, link, summary))
    
    return articles

def save_to_db(articles):
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, link TEXT, summary TEXT)''')

    for article in articles:
        c.execute("INSERT INTO articles (title, link, summary) VALUES (?, ?, ?)", article)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    articles = scrape_articles()
    save_to_db(articles)
