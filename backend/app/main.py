from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.metrics_api import router as metrics_router

from app.database import initialize_database, save_request
from app.llm import ask_llm
from app.cache import SemanticCache
from app.router import route_query
from app.metrics import (
    calculate_cost,
    start_timer,
    calculate_latency
)

app = FastAPI(
    title="Semantic Cache & Cost-Aware Router",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_database()

app.include_router(metrics_router)


# Semantic cache
cache = SemanticCache(
    similarity_threshold=0.70
)


class AskRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {
        "message": "Semantic Cache & Cost-Aware Router is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask(request: AskRequest):

    start_time = start_timer()

    # 1. Check semantic cache
    cached_result = cache.find(request.query)

    # 2. Cache hit
    if cached_result and cached_result["cache_hit"]:

        latency = calculate_latency(start_time)

        save_request(
            query=request.query,
            cache_hit=True,
            similarity=cached_result["similarity"],
            route="cache",
            model=None,
            input_tokens=0,
            output_tokens=0,
            cost=0.0,
            latency_ms=latency
        )

        return {
            "query": request.query,
            "answer": cached_result["answer"],
            "cache_hit": True,
            "similarity": cached_result["similarity"],
            "route": "cache",
            "model": None,
            "input_tokens": 0,
            "output_tokens": 0,
            "cost": 0.0,
            "latency_ms": latency
        }

    # 3. Cache miss → call LLM
    # 3. Cache miss → route query to appropriate model
    routing_result = route_query(request.query)

    llm_result = ask_llm(
        request.query,
        model=routing_result["model"]
    )
    answer = llm_result["answer"]

    input_tokens = llm_result["input_tokens"]
    output_tokens = llm_result["output_tokens"]

    cost = calculate_cost(
    routing_result["model"],
    input_tokens,
    output_tokens
    )

    latency = calculate_latency(start_time)

    save_request(
        query=request.query,
        cache_hit=False,
        similarity=(
            cached_result["similarity"]
            if cached_result
            else None
        ),
        route=routing_result["route"],
        model=routing_result["model"],
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost=cost,
        latency_ms=latency
    )

    # 4. Store the new answer in cache
    cache.add(
        request.query,
        answer
    )
    # 5. Return response
    return {
    "query": request.query,
    "answer": answer,
    "cache_hit": False,
    "similarity": (
        cached_result["similarity"]
        if cached_result
        else None
    ),
    "route": routing_result["route"],
    "model": routing_result["model"],
    "input_tokens": input_tokens,
    "output_tokens": output_tokens,
    "cost": cost,
    "latency_ms": latency
}