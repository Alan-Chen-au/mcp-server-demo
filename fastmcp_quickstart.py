"""
FastMCP quickstart example with CORS support for MCP Inspector.
Simplified version serving MCP at root path.

Run from the repository root:
    uv run fastmcp_quickstart.py
"""

from mcp.server.fastmcp import FastMCP
import os
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from starlette.applications import Starlette


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


# Run with streamable HTTP transport
if __name__ == "__main__":
    # Get port from Render (Render sets PORT automatically)
    port = int(os.environ.get("PORT", 8000))

    # Get the MCP ASGI app
    app = mcp.streamable_http_app()

    # Wrap in Starlette to add CORS
    root_app = Starlette()
    root_app.mount("/", app)

    # Add CORS middleware
    root_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # Run Uvicorn
    print(f"🚀 Starting MCP server on port {port}")
    print(f"📍 MCP endpoint: http://0.0.0.0:{port}/")

    uvicorn.run(
        root_app,
        host="0.0.0.0",
        port=port,
        log_level="info",
    )