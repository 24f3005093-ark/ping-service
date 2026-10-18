import time
import uuid
from collections import defaultdict, deque

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

MY_EMAIL = "24f3005093@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://app-2v71vo.example.com"
EXAM_ORIGIN = "https://exam.sanand.workers.dev"

MAX_REQUESTS = 8
WINDOW_SECONDS = 10

app = FastAPI()

hits = defaultdict(deque)

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client_id = request.headers.get("X-Client-Id") or (
        request.client.host if request.client else "unknown"
    )
    now = time.time()
    q = hits[client_id]

    while q and now - q[0] > WINDOW_SECONDS:
        q.popleft()

    if len(q) >= MAX_REQUESTS:
        return JSONResponse({"detail": "Too Many Requests"}, status_code=429)

    q.append(now)
    return await call_next(request)

@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN, EXAM_ORIGIN],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["X-Request-ID", "X-Client-Id", "Content-Type"],
    expose_headers=["X-Request-ID"],
)

@app.get("/ping")
async def ping(request: Request):
    return {"email": MY_EMAIL, "request_id": request.state.request_id}