#api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from main import run_pipeline
from rag_engine import ask_question


app = FastAPI(
    title="AI Video Assistant API"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class VideoRequest(BaseModel):
    source: str
    language: str = "english"


class ChatRequest(BaseModel):
    question: str


# --------------------------------------------------
# Store current RAG chain
# --------------------------------------------------

rag_chain = None


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "AI Video Assistant API is running"
    }


# --------------------------------------------------
# Process Video
# --------------------------------------------------

@app.post("/process")
def process_video(request: VideoRequest):

    global rag_chain

    try:

        result = run_pipeline(
            request.source,
            request.language
        )

        rag_chain = result["rag_chain"]

        return {
            "title": result["title"],
            "transcript": result["transcript"],
            "summary": result["summary"],
            "action_items": result["action_items"],
            "key_decisions": result["key_decisions"],
            "open_questions": result["open_questions"],
            "claims": result["claims"],
            "verified_claims": result["verified_claims"],
        }

    except Exception as e:

        print("Pipeline error:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# Chat
# --------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    global rag_chain

    if rag_chain is None:

        raise HTTPException(
            status_code=400,
            detail="Please process a video first."
        )

    try:

        answer = ask_question(
            rag_chain,
            request.question
        )

        return {
            "answer": answer
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )