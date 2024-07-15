from apscheduler.schedulers.blocking import BlockingScheduler
from scraper import scrape_articles, save_to_db

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', minutes=30)
def scheduled_scrape():
    articles = scrape_articles()
    save_to_db(articles)
    print("Scraped and saved new articles")

scheduler.start()
