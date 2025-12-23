import typer
import uvicorn

app = typer.Typer()


@app.command()
def caching_proxy(origin: str = "google.com", port: int = 3000):
    uvicorn.run("server:app", port=port, reload=True)


if __name__ == "__main__":
    app()
