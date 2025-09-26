#!/usr/bin/env python3
# -------------------------------------------------------
# src/main.py
# -------------------------------------------------------
# Purpose Summary:
#   - Public-safe FastAPI demo for cfo-router-2.0.
#   - Provides /api/healthz and /api/query (echo) with no provider calls.
# Audit:
#   - All actions print ISO 8601 UTC timestamps.
#   - Fails safe with 4xx/5xx and never exposes internal details.
# -------------------------------------------------------

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timezone
import os

# -------------------------------------------------------
# Function: ts
# Purpose:
#   - Generate ISO 8601 UTC timestamp.
# Audit:
#   - Used in logs for traceability.
# -------------------------------------------------------
def ts() -> str:
    return datetime.now(timezone.utc).isoformat()

# -------------------------------------------------------
# FastAPI App
# -------------------------------------------------------
app = FastAPI(title="cfo-router-demo", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# -------------------------------------------------------
# Model: ChatQuery
# Purpose:
#   - Request schema for POST /api/query.
# Audit:
#   - Ensures payload includes a 'message' field.
# -------------------------------------------------------
class ChatQuery(BaseModel):
    message: str

# -------------------------------------------------------
# Route: /api/healthz [GET]
# Purpose:
#   - Health check endpoint.
# Audit:
#   - Prints timestamped log on each call.
# -------------------------------------------------------
@app.get("/api/healthz")
def healthz():
    print(f"[{ts()}] HEALTHZ ok")
    return {"status": "ok"}

# -------------------------------------------------------
# Route: /api/query [POST]
# Purpose:
#   - Echo endpoint for demo purposes.
# Audit:
#   - Logs message length with timestamp.
#   - Returns canned response with meta.
# -------------------------------------------------------
@app.post("/api/query")
def query(q: ChatQuery = Body(...)):
    text = (q.message or "").strip()
    print(f"[{ts()}] QUERY len={len(text)}")
    if not text:
        raise HTTPException(status_code=400, detail="message required")
    return {
        "response": f"(demo) Received: {text}",
        "meta": {"source": "cfo-router-demo", "ts": ts()}
    }

# -------------------------------------------------------
# Entrypoint
# Purpose:
#   - Start FastAPI app with uvicorn for local demo.
# Audit:
#   - Logs startup timestamp, bind host, and port.
# -------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    host = os.getenv("ROUTER_BIND", "0.0.0.0")
    port = int(os.getenv("ROUTER_PORT", "8001"))
    print(f"[{ts()}] starting cfo-router-demo on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
