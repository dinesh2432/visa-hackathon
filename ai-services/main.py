import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from schemas import ExtractedMetadata
from prompt import DQ_PROMPT
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

app = FastAPI(
    title="DQS-AI Agent",
    description="Data Quality Service powered by GenAI",
    version="1.0.0"
)

GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY or not GROQ_API_KEY.startswith("gsk_"):
    raise RuntimeError("❌ Invalid or missing GROQ_API_KEY")

llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0.2,
    api_key=GROQ_API_KEY
)

dq_chain = DQ_PROMPT | llm | StrOutputParser()


@app.post("/analyze-dqs")
async def analyze_dqs(payload: dict):
    """
    Analyze data quality from extracted metadata.
    
    Args:
        payload: Dictionary containing dataset metadata
        
    Returns:
        JSON response with GenAI insights
    """
    try:
        metadata = ExtractedMetadata.normalize(payload)
        response = dq_chain.invoke({
            "metadata": metadata.model_dump()
        })
        return {
            "status": "success",
            "genai_insights": response
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid payload format: {str(e)}"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze data quality: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint with service info"""
    return {
        "message": "DQS-AI Agent is running",
        "endpoints": {
            "analyze": "/analyze-dqs",
            "docs": "/docs"
        },
        "model": GROQ_MODEL,
        "api_key_configured": bool(GROQ_API_KEY),
        "api_key:" : GROQ_API_KEY
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model": GROQ_MODEL,
        "api_key_configured": bool(GROQ_API_KEY)
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": str(exc),
            "type": type(exc).__name__
        }
    )


if __name__ == "__main__":
    print("=" * 50)
    print("🚀 DQS-AI Agent")
    print("=" * 50)
    print(f"📦 Model: {GROQ_MODEL}")
    print(f"🔑 API Key: {'✅ Configured' if GROQ_API_KEY else '❌ Not set'}")
    print("\n💡 Run with: uvicorn main:app --reload")
    print("📚 Docs at: http://localhost:8000/docs")
    print("=" * 50)