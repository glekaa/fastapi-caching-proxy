import json
import os
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request, Response
from redis.asyncio import Redis

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient() as http_client:
        async with Redis.from_url("redis://localhost:6379") as redis_client:
            app.state.http_client = http_client
            app.state.redis_client = redis_client
            yield


app = FastAPI(lifespan=lifespan)


@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
)
async def catch_all(request: Request, path: str):
    http_client: httpx.AsyncClient = request.app.state.http_client
    url = f"{os.getenv('ORIGIN')}/{path}"

    redis_client: Redis = request.app.state.redis_client
    sorted_params = sorted(request.query_params.items())
    cache_key = f"{request.method}:{url}:{sorted_params}"

    if request.method == "GET":
        cached_json = await redis_client.get(cache_key)
        if cached_json:
            data = json.loads(cached_json)
            headers = data["headers"]
            headers["X-Cache"] = "HIT"

            return Response(
                content=data["body"],
                status_code=data["status"],
                media_type="application/json",
                headers=headers,
            )

    req_headers = dict(request.headers)
    req_headers.pop("host", None)

    response = await http_client.request(
        method=request.method,
        url=url,
        headers=req_headers,
        params=request.query_params,
        json=await request.json() if request.method in ["POST", "PUT"] else None,
    )

    if request.method == "GET" and response.status_code == 200:
        cache_data = {
            "body": response.text,
            "status": response.status_code,
            "headers": dict(response.headers),
        }
        await redis_client.set(cache_key, json.dumps(cache_data), ex=900)

    response_headers = dict(response.headers)
    response_headers["X-Cache"] = "MISS"

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=response.headers.get("content-type"),
        headers=response_headers,
    )
