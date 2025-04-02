from fastapi import FastAPI, HTTPException
import requests
import os
from pydantic import BaseModel

app = FastAPI()

# Securely get API key from environment variable
API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.ai/v1/completions"

class RequestData(BaseModel):
    user_input: str

@app.get("/")
def read_root():
    return {"message": "FastAPI Mistral app is running!"}

@app.post("/generate_tasks")
def generate_tasks(data: RequestData):
    """
    Process user request using Together.AI and return a structured task checklist.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Missing API key")
    
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",  # Using a serverless model
        "prompt": f"Convert this request into a checklist: {data.user_input}",
        "max_tokens": 100
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    response = requests.post(TOGETHER_API_URL, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Together.AI API error")
    
    result = response.json()
    checklist = result.get("choices", [{}])[0].get("text", "No response").strip()
    
    return {"tasks": checklist.split("\n")}
