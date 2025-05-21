import os
from fastapi import FastAPI, Request
from goose import Goose
import uvicorn

# Initialize FastAPI
app = FastAPI(title="Goose Agent API")

# Initialize Goose with API key from environment variable
api_key = os.environ.get("LLM_API_KEY")
goose = Goose(api_key=api_key)

# System prompt
system_prompt = """
You are running in a Zerops container. You can help with development tasks.
"""

@app.get("/status")
async def status():
    return {"status": "OK"}

@app.get("/")
async def root():
    return {"message": "Goose Agent is running"}

@app.post("/query")
async def query(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    
    # Process with Goose
    conversation = goose.start_conversation(system_prompt=system_prompt)
    response = conversation.send_message(user_message)
    
    return {"response": response}

# This allows running directly with python app.py
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
