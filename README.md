# Caching Proxy CLI

A high-performance CLI tool that starts a caching proxy server. It forwards requests to an origin server and caches the responses in Redis to speed up subsequent requests. Built with [FastAPI](https://fastapi.tiangolo.com/), [Redis](https://redis.io/), and [Typer](https://typer.tiangolo.com/).

## Features

- Forward requests to any origin server and cache responses in Redis
- Returns `X-Cache: HIT` or `MISS` headers to indicate cache status
- Clear cache with a single `--clear-cache` flag

## Prerequisites

- **Python 3.13+**
- **Docker** (for running Redis)

## Quick Start

### 1. Start Redis
The tool requires a running Redis instance. The easiest way is using the provided Docker Compose file:

```bash
docker compose up -d
```

### 2. Run the Proxy

#### Option A: Run Directly (No Installation)
From the project directory, run without installing:

```bash
# Using uv (recommended)
uv run caching-proxy --port 3000 --origin https://dummyjson.com

# Using pip
python -m main --port 3000 --origin https://dummyjson.com
```

#### Option B: Install as a Package
Install the tool to use it from anywhere:

```bash
uv pip install .   # or: pip install .
```

Then run:

```bash
caching-proxy --port 3000 --origin https://dummyjson.com
```

## Usage

### CLI Options

| Option          | Description                                      | Default                 |
|-----------------|--------------------------------------------------|-------------------------|
| `--port`        | The port on which the proxy server will run      | `3000`                  |
| `--origin`      | The URL of the server to forward requests to     | `https://dummyjson.com` |

### Start the Server
```bash
caching-proxy --port <number> --origin <url>
```

**Example:**
Forward requests to `dummyjson.com` on local port 3000:
```bash
caching-proxy --port 3000 --origin https://dummyjson.com
```

### Make a Request
Now you can request `http://localhost:3000/products` and it will be proxied to `https://dummyjson.com/products`.

*   **First Request**: `X-Cache: MISS` (Fetched from server, stored in Redis)
*   **Second Request**: `X-Cache: HIT` (Served instantly from Redis)

### Clear Cache
To clear the Redis cache, run `caching-proxy` with the `--clear-cache` flag as a standalone command:

```bash
caching-proxy --clear-cache
```

This clears all cached responses and exits immediately.

### Extras

This Repo serves as a solution to [Roadmap.sh Caching Server Problem](https://roadmap.sh/projects/caching-server)
