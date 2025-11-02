"""
Example FastAPI backend for the agent-chat-ui
This is a simple echo bot that demonstrates the required API structure.

Install dependencies:
    pip install fastapi uvicorn

Run:
    python example_backend.py

The server will start at http://localhost:8000
"""

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="Example Chat Backend",
    description="Simple example backend for agent-chat-ui",
    version="1.0.0"
)

# Enable CORS for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    """A single message in the conversation"""
    role: str  # "user", "assistant", or "system"
    content: str


class ChatRequest(BaseModel):
    """Request body for the /chat endpoint"""
    message: str
    history: Optional[List[ChatMessage]] = []  # Kept for backwards compatibility, but not used


class ChatResponse(BaseModel):
    """Response body for the /chat endpoint"""
    message: str
    role: str = "assistant"


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Example Chat Backend API",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}


@app.post("/chat")
async def chat(
    request: ChatRequest,
    authorization: Optional[str] = Header(None)
) -> ChatResponse:
    """
    Main chat endpoint
    
    This is a simple echo bot that repeats what you say.
    Replace this logic with your own AI/LLM integration.
    
    Note: History is now managed by the backend, not sent from frontend.
    If you need conversation history, implement session management here.
    """
    
    # Optional: Check API key if provided
    if authorization:
        token = authorization.replace("Bearer ", "")
        # You can validate the token here
        # For this example, we'll accept any token
        print(f"Received token: {token}")
    
    # Simple echo response - just repeat the message
    response_text = request.message
    
    # History is no longer sent from frontend to keep it lightweight
    # If you need conversation history, implement it here using:
    # - Database (PostgreSQL, MongoDB, etc.)
    # - Redis cache with session IDs
    # - In-memory storage with user sessions
    
    # Here's where you would integrate your AI/LLM
    # For example:
    # - Call OpenAI API
    # - Use a local LLM
    # - Integrate with LangChain
    # - Connect to your custom agent
    
    return ChatResponse(
        message=response_text,
        role="assistant"
    )


if __name__ == "__main__":
    print("Starting Example Chat Backend...")
    print("Server will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
