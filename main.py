from fastapi import FastAPI
from pydantic import BaseModel
import openai
import requests
import os

app = FastAPI()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # Nebo ho můžeš přímo napsat zde na test

class Message(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(message: Message):
    print("User prompt:", message.prompt)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message.prompt}
        ]
    )
    reply = response.choices[0].message.content
    return {"reply": reply}

@app.post("/news")
async def get_news(message: Message):
    print("News topic:", message.prompt)
    url = f"https://newsapi.org/v2/everything?q={message.prompt}&language=cs&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    articles = [{"title": article["title"], "url": article["url"]} for article in data.get("articles", [])]

    return {"news": articles}

@app.get("/")
def read_root():
    return {"message": "Hello from your AI assistant!"}
