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
    Process the user request using Together.AI (Mistral model)
    and return a structured task checklist.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Missing API key")
    
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "prompt": (
            "Convert this request into a plain text checklist. Each item should be on a new line, "
            "without any markdown symbols or extra text. Only list the tasks.\n\n"
            "User request: " + data.user_input
        ),
        "max_tokens": 100
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    response = requests.post(TOGETHER_API_URL, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Mistral API error")
    
    result = response.json()
    raw_text = result.get("choices", [{}])[0].get("text", "").strip()

    # Split text by newlines and remove unwanted characters
    lines = raw_text.split("\n")
    checklist = []
    for line in lines:
        # Remove leading/trailing spaces and any asterisks, hyphens, or bullets
        cleaned_line = line.strip(" -*")
        # Skip empty lines or lines that are not valid tasks (like "Checklist:" or just ".")
        if not cleaned_line:
            continue
        if cleaned_line.lower().startswith("checklist"):
            continue
        checklist.append(cleaned_line)
    
    return {"tasks": checklist}
