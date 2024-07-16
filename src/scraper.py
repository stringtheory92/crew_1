import requests
from bs4 import BeautifulSoup
import sqlite3

def scrape_article_titles_links():
    url = 'https://news.google.com/search?q=artificial+intelligence&hl=en-US&gl=US&ceid=US:en'
    headers = {}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')


    articles = []
    for item in soup.find_all('article', class_='IFHyqb'):
      
        title_tag = item.find('a', class_='JtKRv')
        title = title_tag.text if title_tag else 'No title available'

        link = title_tag['href'] if title_tag else ''
        if link.startswith('.'):
            link = f"https://news.google.com{link[1:]}" 

        summary_tag = item.find('div', class_='IL9Cne')
        summary = summary_tag.text if summary_tag else 'No summary available'

        articles.append((title, link, summary))
    
    return articles

def save_to_db(articles):
    # print(articles)
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, link TEXT, summary TEXT)''')
    print("Table created")

    for article in articles:
        c.execute("INSERT INTO articles (title, link, summary) VALUES (?, ?, ?)", article)
        print(f"Updated article in db: {article}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    articles = scrape_article_titles_links()
    save_to_db(articles)
    