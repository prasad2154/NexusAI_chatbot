"""FastAPI proxy that forwards chat messages to a local Ollama model.

The Streamlit front‑end sends a POST request to ``/chat`` with JSON:
    {"message": "Your question"}
The server forwards this to Ollama's chat API (http://localhost:11434/api/chat) and returns the model's reply.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "NexusAI FastAPI Backend is running!",
        "endpoints": {
            "chat": "POST /chat",
            "ping": "GET /ping",
            "docs": "GET /docs"
        }
    }


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama2"  # change to any model you have pulled with Ollama

class Message(BaseModel):
    message: str

@app.post("/chat")
async def chat(msg: Message):
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": msg.message}],
        "stream": False,
    }
    # Try the newer /api/chat endpoint first; if it returns 404, fallback to /api/generate
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(OLLAMA_URL, json=payload, timeout=30)
        if resp.status_code == 404:
            # Older Ollama versions expose /api/generate instead of /api/chat
            fallback_url = OLLAMA_URL.replace("/chat", "/generate")
            async with httpx.AsyncClient() as client:
                resp = await client.post(fallback_url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        # Newer /api/chat returns {"message": {"content": "..."}}
        # Fallback /api/generate returns {"response": "..."}
        if "message" in data:
            reply = data["message"].get("content", "")
        else:
            reply = data.get("response", "")
        return {"reply": reply}
    except httpx.ConnectError:
        return {"error": "Could not connect to Ollama at http://localhost:11434. Ensure Ollama is running and the model is loaded."}
    except Exception as e:
        return {"error": str(e)}

@app.get("/ping")
async def ping():
    """Simple health‑check endpoint used to verify the service is running."""
    return {"status": "ok"}
