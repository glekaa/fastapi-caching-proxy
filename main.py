import typer

app = typer.Typer()


@app.command()
def caching_proxy(origin: str = "google.com", port: int = 3000):
    print(f"port: {port}, origin: {origin}")


if __name__ == "__main__":
    app()
