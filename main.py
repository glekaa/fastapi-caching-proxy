import os

import typer
import uvicorn

app = typer.Typer()


@app.command()
def caching_proxy(
    port: int = 3000,
    origin: str = "https://google.com",
):
    os.environ["ORIGIN"] = origin
    uvicorn.run("server:app", port=port, reload=True)


if __name__ == "__main__":
    app()
