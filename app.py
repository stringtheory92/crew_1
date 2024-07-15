from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import pipeline
import sqlite3
import crewai

app = FastAPI()

def get_latest_articles():
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    c.execute("SELECT * FROM articles ORDER BY id DESC LIMIT 5")
    articles = c.fetchall()
    conn.close()
    return articles

@crewai.task
def query_llm(query):
    articles = get_latest_articles()
    context = " ".join([article[2] for article in articles])
    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')
    prompt = f"Context: {context}\nQuery: {query}\nAnswer:"
    response = generator(prompt, max_length=200)
    return response[0]['generated_text']

class QueryModel(BaseModel):
    query: str

@app.get('/latest-articles')
def latest_articles():
    articles = get_latest_articles()
    return articles

@app.post('/query')
async def handle_query(query: QueryModel):
    response = crewai.run_task(query_llm, query=query.query)
    return {"response": response}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
