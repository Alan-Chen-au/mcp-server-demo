"""
FastMCP quickstart example.

Run from the repository root:
    uv run fastmcp_quickstart.py
"""

from mcp.server.fastmcp import FastMCP
import os
import uvicorn


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

    # FastMCP creates an ASGI server internally
    # We must access the underlying FastAPI app
    app = mcp.fastmcp_app  # <-- This is the actual ASGI app

    # Run Uvicorn manually so we can control the host/port for Render
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
    )
