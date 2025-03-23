from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx
import json
import uvicorn
from typing import Optional, Dict, Any
import os
import asyncio
from balldontlie import BalldontlieAPI
from pathlib import Path

app = FastAPI()

####################################
# Load .env file
####################################

OPEN_WEBUI_DIR = Path(__file__).parent  # the path containing this file
print(OPEN_WEBUI_DIR)

BACKEND_DIR = OPEN_WEBUI_DIR.parent  # the path containing this file
BASE_DIR = BACKEND_DIR.parent  # the path containing the backend/

print(BACKEND_DIR)
print(BASE_DIR)

try:
    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv(str(BASE_DIR / ".env")))
except ImportError:
    print("dotenv not installed, skipping...")

# Initialize the balldontlie API
balldontlie_api = BalldontlieAPI(api_key=os.environ.get("BALLDONTLIE_API_KEY", None))

# Configure the Ollama endpoint - you can change this to your Ollama instance
OLLAMA_API_URL = "http://localhost:11434"

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
    body = await request.body()
    data = json.loads(body)
    print("data", data)
    
    # Check if this is a streaming request
    is_streaming = data.get("stream", True)  # Default to True for backward compatibility
    
    async def generate_response():
        try:
            if "messages" in data:
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
                if is_streaming:
                    # For streaming responses, yield chunks as they come
                    async for chunk in response.aiter_bytes():
                        yield chunk
                else:
                    # For non-streaming responses, accumulate the full response
                    full_response = b""
                    async for chunk in response.aiter_bytes():
                        full_response += chunk
                    yield full_response
                    
        except Exception as e:
            print(f"Error in chat: {str(e)}")
            yield json.dumps({"error": str(e)}).encode()
    
    # Set the appropriate content type based on streaming vs non-streaming
    return StreamingResponse(
        generate_response(),
        media_type="application/x-ndjson" if is_streaming else "application/json"
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
    uvicorn.run(app, host="0.0.0.0", port=11435) 