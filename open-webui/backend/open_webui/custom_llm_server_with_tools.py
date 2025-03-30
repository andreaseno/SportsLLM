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
import ollama
from ollama_tools import  generate_function_description, use_tools
import traceback
from nba_tools import (
    get_player_injuries, 
    get_game_odds, 
    get_head_to_head_stats, 
    get_league_leaders, 
    get_player_info, 
    # get_player_season_stats, 
    get_team_info, 
    get_team_standings
    )

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

def query_model(messages, tools, model='llama3.1:latest'):
    print("query_model")
    print(messages)
    response = ollama.chat(
        model=model,
        messages=messages,
        tools=tools,
        stream=True,
    )
    return response

# def get_player_stats(Name:str) -> str:
#     """Get the statistics for an NBA player.

#     Args:
#         Name: The name of the player to get the statistics for.

#     Returns:
#         A string with the statistics for the player.
#     """
#     print(f"\n\n\n\n\nget_player_stats: {Name}\n\n\n\n\n")
#     # base_url = f"https://wttr.in/{city}?format=j1"
#     # response = requests.get(base_url)
#     # data = response.json()
#     return f"""The statistics for {Name} are: {Name}"""

tools = [
    generate_function_description(get_player_injuries),
    generate_function_description(get_game_odds),
    generate_function_description(get_head_to_head_stats),
    generate_function_description(get_league_leaders),
    generate_function_description(get_player_info),
    # generate_function_description(get_player_season_stats),
    generate_function_description(get_team_info),
    generate_function_description(get_team_standings),
]
functions = {function["function"]["name"]: globals()[function["function"]["name"]] for function in tools }


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
    # print("data", data)
    
    is_streaming = data.get("stream", True)
    
    async def generate_response():
        try:
            print("generate_response")
            if "messages" in data:
                if not any(msg["role"] == "system" for msg in data["messages"]):
                    data["messages"].insert(0, {
                        "role": "system",
                        "content": "You are an assistant with access to tools, if you do not have a tool to deal with the user's request but you think you can answer do it so, if not explain your capabilities"
                    })
                
            messages = data.get("messages", [{
                        "role": "system",
                        "content": "You are an assistant with access to tools, if you do not have a tool to deal with the user's request but you think you can answer do it so, if not explain your capabilities"
                    }])
            function_call = True
            if "metadata" in data:
                # TODO: Handle different tasks 
                if "task" in data["metadata"]:
                    task = data["metadata"]["task"]
                    if task == "tags_generation":
                        print("tags_generation")
                        function_call = False
                    elif task == "title_generation":
                        print("title_generation")
                        function_call = False
                    elif task == "autocomplete_generation":
                        print("autocomplete_generation")
                        function_call = False
                else:
                    print("chat task")
                    print("data", data)
            
            if not function_call:
                async with async_client.stream(
                    "POST",
                    f"{OLLAMA_API_URL}/api/chat",
                    json={
                        'model': 'llama3.2:1b', 
                        'messages': data['messages'],
                        'stream': is_streaming
                    },
                    headers={"Content-Type": "application/json"}
                ) as response:
                    async for chunk in response.aiter_bytes():
                        yield chunk
            else:    
                # For function calling path
                messages = data.get('messages', [])
                
                max_retries = 10
                retry_count = 0
                tool_call_success = False

                while retry_count < max_retries and not tool_call_success:
                    try:
                        async with async_client.stream(
                            "POST",
                            f"{OLLAMA_API_URL}/api/chat",
                            json={
                                'model': data.get('model', 'llama3.2:1b'),
                                'messages': messages,
                                'tools': tools,
                                'stream': is_streaming
                            },
                            headers={"Content-Type": "application/json"}
                        ) as response:
                            accumulated_response = b""
                            tool_calls = None
                            async for chunk in response.aiter_bytes():
                                try:
                                    # Decode and parse the JSON chunk
                                    chunk_data = json.loads(chunk.decode('utf-8'))
                                    print("Function call chunk:", chunk_data)  # Debug print
                                    
                                    if 'message' in chunk_data and 'tool_calls' in chunk_data['message']:
                                        tool_calls = chunk_data['message']['tool_calls']
                                        break
                                    
                                    if is_streaming:
                                        yield chunk
                                    else:
                                        accumulated_response += chunk
                                except json.JSONDecodeError:
                                    # Handle incomplete JSON chunks
                                    if is_streaming:
                                        yield chunk
                                    else:
                                        accumulated_response += chunk
                            
                            if not is_streaming:
                                print("Full response:", accumulated_response)  # Debug print
                                yield accumulated_response

                        if tool_calls:
                            result = use_tools(tool_calls, functions)
                            tool_call_success = True
                        # else:
                        #     # If no tool calls were found, add a message asking for proper tool usage
                        #     messages.append({
                        #         "role": "system",
                        #         "content": "Please provide a properly formatted tool call. Your previous response did not include any tool calls."
                        #     })
                    except Exception as e:
                        print(f"Tool call attempt {retry_count + 1} failed: {str(e)}")
                        retry_count += 1
                        if retry_count < max_retries:
                            # Add a message to guide the model to provide better formatting
                            # messages.append({
                            #     "role": "system",
                            #     "content": f"The previous tool call failed due to: {str(e)}. Please provide a properly formatted tool call."
                            # })
                            print()
                        else:
                            # If we've exhausted retries, yield an error message
                            error_response = {"error": f"Failed to execute tool call after {max_retries} attempts: {str(e)}"}
                            yield json.dumps(error_response).encode()
                            return

                if tool_call_success:
                    messages.append({
                        "role": "tool",
                        "content": result
                    })
                    
                    async with async_client.stream(
                        "POST",
                        f"{OLLAMA_API_URL}/api/chat",
                        json={
                            'model': data.get('model', 'llama3.2:1b'),
                            'messages': messages,
                            'stream': is_streaming
                        },
                        headers={"Content-Type": "application/json"}
                    ) as response:
                        accumulated_response = b""
                        async for chunk in response.aiter_bytes():
                            if is_streaming:
                                yield chunk
                            else:
                                accumulated_response += chunk

                        if not is_streaming:
                            print("Full response:", accumulated_response)  # Debug print
                            yield accumulated_response

        except Exception as e:
            print(f"Error in chat: {str(e)}")
            print(traceback.format_exc())
            yield json.dumps({"error": str(e)}).encode()
    
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
                
            if "metadata" in data:
                # TODO: Handle different tasks 
                if "task" in data["metadata"]:
                    task = data["metadata"]["task"]
                    if task == "tags_generation":
                        print("tags_generation")
                    elif task == "title_generation":
                        print("title_generation")
                     
                else:
                    print("chat task")
                        
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