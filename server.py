import os
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request, Response

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient() as client:
        app.state.client = client
        yield


app = FastAPI(lifespan=lifespan)


@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
)
async def catch_all(request: Request, path: str):
    client: httpx.AsyncClient = request.app.state.client

    response = await client.request(
        method=request.method,
        url=f"{os.getenv('ORIGIN')}/{path}",
        params=request.query_params,
    )

    return Response(content=response.content, status_code=response.status_code)
