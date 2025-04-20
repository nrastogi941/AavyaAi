import os
import asyncio
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from session import (
    start_agent_session, 
    agent_to_client_messaging,
    client_to_agent_messaging
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path("static")
print(f"Static directory: {STATIC_DIR}")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def root():
    """Serves the index.html"""
    # return "Welcome to AavyaAI! Your 24*7 Indian Legal Assistant. Visit 'https://aavyaai.com'"
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))



@app.websocket("/chat/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """Client websocket endpoint"""

    # Wait for client connection
    #Client connects to server over WebSocket.
    await websocket.accept()   #accepts the websocket connection — like picking up a phone call.
    print(f"Client #{session_id} connected")

    # Start agent session
    session_id = str(session_id)
    live_events, live_request_queue = start_agent_session(session_id)

    # Start tasks
    agent_to_client_task = asyncio.create_task(    #the server listens for messages from the agent and sends them to the client.
        agent_to_client_messaging(websocket, live_events)
    )
    client_to_agent_task = asyncio.create_task(  #the server receives messages from the client and forwards them to the agent.
        client_to_agent_messaging(websocket, live_request_queue, session_id)
    )
    await asyncio.gather(agent_to_client_task, client_to_agent_task)

    # Disconnected
    print(f"Client #{session_id} disconnected")