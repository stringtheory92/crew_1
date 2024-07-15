import crewai
from scraper import scrape_articles, save_to_db

@crewai.task
def scrape_and_save_articles():
    articles = scrape_articles()
    save_to_db(articles)
    print("Scraped and saved new articles")

# Schedule this task to run every 30 minutes
crewai.schedule(scrape_and_save_articles, interval=30)

@crewai.task(trigger="new_article")
def monitor_and_scrape():
    articles = scrape_articles()
    save_to_db(articles)
    print("New AI-related articles found and saved.")

# Define the trigger based on website content changes
crewai.monitor("https://example.com/ai-news", keywords=["AI", "machine learning", "deep learning"], callback=monitor_and_scrape)

if __name__ == "__main__":
    crewai.run()
