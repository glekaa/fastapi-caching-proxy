import os

import redis
import typer
import uvicorn

app = typer.Typer()


def clear_cache_callback(value: bool):
    if value:
        try:
            redis_client = redis.Redis.from_url("redis://localhost:6379")
            redis_client.flushdb()
            typer.echo("Cache has been cleared successfully")
        except redis.ConnectionError:
            typer.echo("Failed to clear cache")
        raise typer.Exit()


@app.command()
def caching_proxy(
    port: int = 3000,
    origin: str = "https://google.com",
    clear_cache: bool = typer.Option(
        False, "--clear-cache", callback=clear_cache_callback, is_eager=True
    ),
):
    os.environ["ORIGIN"] = origin
    uvicorn.run("server:app", port=port, reload=True)


if __name__ == "__main__":
    app()
