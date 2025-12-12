"""
FastMCP quickstart example with CORS support for MCP Inspector.

Run from the repository root:
    uv run fastmcp_quickstart.py
"""

from mcp.server.fastmcp import FastMCP
import os
import uvicorn
import contextlib
from starlette.middleware.cors import CORSMiddleware
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount

# Create an MCP server
mcp = FastMCP("Demo", json_response=True)


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


# Health check endpoint
async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "MCP Server Demo"})


# Create a lifespan context manager to run the session manager
@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with mcp.session_manager.run():
        yield


# Run with streamable HTTP transport
if __name__ == "__main__":
    # Get port from Render (Render sets PORT automatically)
    port = int(os.environ.get("PORT", 8000))

    # Mount the StreamableHTTP server to the existing ASGI server
    app = Starlette(
        routes=[
            Route("/health", health_check),
            Mount("/mcp", app=mcp.streamable_http_app()),
        ],
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # Run Uvicorn
    print(f"🚀 Starting MCP server on port {port}")
    print(f"📍 MCP endpoint: http://0.0.0.0:{port}/mcp")
    print(f"💚 Health check: http://0.0.0.0:{port}/health")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
    )