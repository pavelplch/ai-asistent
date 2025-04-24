from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Message(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(message: Message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": message.prompt}
        ]
    )
    reply = response.choices[0].message["content"]
    return {"reply": reply}

@app.get("/")
def read_root():
    return {"message": "Hello from your AI assistant!"}
