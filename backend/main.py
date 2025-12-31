from pathlib import Path
from typing import List

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.core.language_utils import detect_language, translate
from app.agents.rag_pipeline import (
    build_vector_store_from_file,
    retrieve_docs,
    run_rag,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    upload_dir = Path("uploaded")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    chunks = build_vector_store_from_file(str(file_path))
    return {"status": "ok", "chunks_added": chunks}


@app.post("/rag-chat")
def rag_chat(request: ChatRequest):
    # לוקחים את ההודעה האחרונה של המשתמש
    user_message = next(
        (m.content for m in reversed(request.messages) if m.role == "user"),
        None
    )

    if not user_message:
        return {"reply": "No user message provided."}

    answer = run_rag(user_message)
    return {"reply": answer}

