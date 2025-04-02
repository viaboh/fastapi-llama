from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel

app = FastAPI()

# Together.AI API Key
API_KEY = "642fa34d3d0c6853f764e84eb4c5d26a1eff5eb61ebaf50270b0b21d1ab558e9"
LLAMA_API_URL = "https://api.together.ai/v1/completions"

class RequestData(BaseModel):
    user_input: str

@app.post("/generate_tasks")
def generate_tasks(data: RequestData):
    """
    Process user request using Llama and return a structured task checklist.
    """
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
    checklist = result.get("choices", [{}])[0].get("text", "No response").strip()
    
    return {"tasks": checklist.split('\n')}

# Run locally with: uvicorn app:app --reload
