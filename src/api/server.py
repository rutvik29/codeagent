import asyncio, uuid
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="CodeAgent API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class CodeRequest(BaseModel):
    task: str
    language: str = "python"
    max_retries: int = 3
    model: str = "gpt-4o"

@app.get("/health")
def health(): return {"status": "ok"}

@app.post("/generate")
async def generate_code(request: CodeRequest):
    return {"task": request.task, "status": "queued", "message": "Add agent wiring to complete"}

@app.websocket("/ws/{session_id}")
async def ws_stream(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        await websocket.send_json({"type": "ready", "session_id": session_id})
        await websocket.send_json({"type": "done"})
    except WebSocketDisconnect:
        pass
