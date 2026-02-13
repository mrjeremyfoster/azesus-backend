from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

# ---------- CONFIG ----------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

# Allow requests from anywhere (important for your app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- DATA MODEL ----------

class QueryRequest(BaseModel):
    query: str

# ---------- ROUTES ----------

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
