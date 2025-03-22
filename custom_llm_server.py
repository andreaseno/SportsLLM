from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx
import json
import uvicorn
from typing import Optional, Dict, Any
import os
import asyncio

app = FastAPI()

# Configure the Ollama endpoint - you can change this to your Ollama instance
OLLAMA_API_URL = "http://localhost:11435"

# Create an async HTTP client
async_client = httpx.AsyncClient(timeout=None)

@app.get("/api/version")
async def get_version():
    """Implement version endpoint to make OpenWebUI happy"""
    return {"version": "0.1.0", "custom_server": True}

@app.get("/api/tags")
async def get_models():
    """
    List available models from Ollama
    """
    print("get_models")
    try:
        print(f"{OLLAMA_API_URL}/api/tags")
        # Properly await the async request
        response = await async_client.get(f"{OLLAMA_API_URL}/api/tags")
        response.raise_for_status()
        models = response.json()
        print(models)
        # You can modify the model list here if you want to filter or transform it
        return models
    except Exception as e:
        print(e)
        return {"error": str(e)}

@app.post("/api/chat")
async def chat(request: Request):
    """
    Main chat endpoint that processes requests from OpenWebUI
    """
    print("chat")
    # Get the raw request body
    body = await request.body()
    data = json.loads(body)
    print("data", data)
    
    async def generate_response():
        try:
            # Add your custom processing here
            if "messages" in data:
                # Example: Add a custom system message if none exists
                if not any(msg["role"] == "system" for msg in data["messages"]):
                    data["messages"].insert(0, {
                        "role": "system",
                        "content": "You are a helpful AI assistant."
                    })
            
            # Forward the modified request to Ollama
            async with async_client.stream(
                "POST",
                f"{OLLAMA_API_URL}/api/chat",
                json=data,
                headers={"Content-Type": "application/json"}
            ) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk
        except Exception as e:
            print(f"Error in chat: {str(e)}")
            yield json.dumps({"error": str(e)}).encode()
    
    return StreamingResponse(
        generate_response(),
        media_type="application/x-ndjson"
    )

@app.post("/api/generate")
async def generate(request: Request):
    """
    Handle direct text generation requests
    """
    print("generate")
    body = await request.body()
    data = json.loads(body)
    
    async def generate_response():
        try:
            # Add your custom processing here
            # Example: Add custom prompt processing
            if "prompt" in data:
                data["prompt"] = f"Process this request: {data['prompt']}"
            
            # Forward to Ollama
            async with async_client.stream(
                "POST",
                f"{OLLAMA_API_URL}/api/generate",
                json=data,
                headers={"Content-Type": "application/json"}
            ) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk
        except Exception as e:
            yield json.dumps({"error": str(e)}).encode()
    
    return StreamingResponse(
        generate_response(),
        media_type="application/json"
    )

if __name__ == "__main__":
    # Run the server on port 11434 to match Ollama's default
    uvicorn.run(app, host="0.0.0.0", port=11434) 