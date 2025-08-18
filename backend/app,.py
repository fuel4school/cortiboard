from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal

app = FastAPI(title="CortiBoard Backend", version="0.1.0")

# Allow local dev frontends (Vite default) — add your deployed domain later
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class KeystrokeEvent(BaseModel):
    type: Literal["keydown", "keyup"]
    key: str
    code: str
    t: float  # ms (performance.now())

class Payload(BaseModel):
    user_id: str
    session_id: str
    events: List[KeystrokeEvent]

@app.get("/")
def root():
    return {"status": "CortiBoard backend running"}

@app.post("/keystrokes")
def receive_keystrokes(payload: Payload):
    # For now, just echo basic stats (you can store/process later)
    num = len(payload.events)
    downs = sum(1 for e in payload.events if e.type == "keydown")
    ups = num - downs
    return {
        "ok": True,
        "received": num,
        "keydowns": downs,
        "keyups": ups,
        "user_id": payload.user_id,
        "session_id": payload.session_id,
    }
