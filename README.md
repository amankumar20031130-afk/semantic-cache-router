# Semantic Cache & Cost-Aware LLM Router

A GenAI infrastructure project that reduces unnecessary LLM calls using semantic caching and routes queries between small and large language models based on query complexity.

## Features

- Semantic caching using Sentence Transformers
- Cosine similarity for cache matching
- Rule-based cost-aware LLM routing
- Small and large model selection
- Token and estimated cost tracking
- Request latency tracking
- SQLite metrics storage
- React dashboard with query playground

## Tech Stack

- Python
- FastAPI
- Sentence Transformers
- Groq API
- SQLite
- React
- Vite
- Tailwind CSS

## How It Works

```text
User Query
    ↓
Semantic Cache
    ↓
Cache Hit → Return Cached Response
    ↓
Cache Miss
    ↓
Cost-Aware Router
    ↓
Small / Large LLM
    ↓
Response + Metrics
    ↓
Store in Cache & SQLite