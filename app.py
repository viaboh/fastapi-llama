from fastapi import FastAPI, HTTPException
import requests
import os
from pydantic import BaseModel
import re

app = FastAPI()

# Securely get API key from environment variable
API_KEY = os.getenv("TOGETHER_API_KEY")
MISTRAL_API_URL = "https://api.together.ai/v1/completions"

class RequestData(BaseModel):
    user_input: str

@app.get("/")
def read_root():
    return {"message": "FastAPI Mistral app is running!"}

@app.post("/generate_tasks")
def generate_tasks(data: RequestData):
    """
    Process user request using Mistral AI and return a structured task checklist.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Missing API key")

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "prompt": f"Convert this request into a clear bullet-point checklist. Do not use markdown formatting: {data.user_input}",
        "max_tokens": 100
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    response = requests.post(MISTRAL_API_URL, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Mistral API error")

    result = response.json()
    raw_text = result.get("choices", [{}])[0].get("text", "").strip()

    # 🛠 Clean up and split properly
    raw_text = raw_text.lstrip(". ")  # Remove unwanted dots and spaces at the start
    checklist = re.split(r"\s*[\n\-•]\s*", raw_text)  # Split by newline, hyphen (-), or bullet (•)
    checklist = [item.strip() for item in checklist if item.strip()]  # Remove empty items

    return {"tasks": checklist}
