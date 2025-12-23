from fastapi import FastAPI, Request

app = FastAPI(debug=True)


@app.api_route(
    "/{full_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
)
async def catch_all(request: Request, full_path: str):
    return {
        "status": "received",
        "path": full_path,
        "method": request.method,
        "query_params": request.query_params,
        "headers": request.headers,
    }
