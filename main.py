from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI

# =========================
# OPENAI CLIENT
# =========================

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# =========================
# FASTAPI APP
# =========================

app = FastAPI()

# Allow requests from anywhere (important for mobile app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DATA MODEL
# =========================

class QueryRequest(BaseModel):
    query: str

# =========================
# ROUTES
# =========================

@app.get("/")
def root():
    return {"status": "AZESUS backend online"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/ask")
async def ask(request: QueryRequest):

    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Empty query")

    try:
        response = client.responses.create(
            model="gpt-5.2",
            input=request.query
        )

        answer = response.output_text

        return {
            "response": answer
        }

    except Exception as e:
        return {
            "error": str(e)
        }
