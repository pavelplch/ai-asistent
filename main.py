from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
import requests

app = FastAPI()

# OpenAI API klíč z prostředí
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# NEWS API klíč z prostředí
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

class Message(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(message: Message):
    print(f"User prompt: {message.prompt}")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message.prompt}
        ]
    )
    reply = response.choices[0].message.content
    return {"reply": reply}

@app.get("/news")
async def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    headlines = [article['title'] for article in data['articles']]
    return {"headlines": headlines}

@app.get("/")
def read_root():
    return {"message": "Hello from your AI assistant!"}
