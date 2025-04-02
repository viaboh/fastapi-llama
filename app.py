from fastapi import FastAPI, HTTPException
import requests
import os
from pydantic import BaseModel

app = FastAPI()

# Securely get API key from environment variable
API_KEY = os.getenv("TOGETHER_API_KEY")
LLAMA_API_URL = "https://api.together.ai/v1/completions"

class RequestData(BaseModel):
    user_input: str

@app.get("/")
def read_root():
    return {"message": "FastAPI Llama app is running!"}

@app.post("/generate_tasks")
def generate_tasks(data: RequestData):
    """
    Process user request using Llama and return a structured task checklist.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Missing API key")

    payload = {
        "model": "meta-llama/Llama-2-7b-chat-hf",
        "prompt": f"Convert this request into a checklist: {data.user_input}",
        "max_tokens": 100
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    response = requests.post(LLAMA_API_URL, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Llama API error")

    result = response.json()
    checklist = result.get("output", "No response").strip()

    return {"tasks": checklist.split("\n")}
