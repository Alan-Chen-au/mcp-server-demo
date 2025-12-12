"""
FastMCP 2.0 server with CORS - FINAL WORKING VERSION

Run from the repository root:
    uv run fastmcp_quickstart.py
"""

from fastmcp import FastMCP
import os
import uvicorn
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

# Create an MCP server
mcp = FastMCP("Demo")


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


# Run with HTTP transport
if __name__ == "__main__":
    # Get port from Render (Render sets PORT automatically)
    port = int(os.environ.get("PORT", 8000))

    print(f"🚀 Starting MCP server on port {port}")
    print(f"📍 MCP endpoint: http://0.0.0.0:{port}/mcp")
    print(f"🌐 CORS enabled for all origins")

    # Configure CORS middleware for browser-based MCP Inspector
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allow all origins for MCP Inspector
            allow_credentials=True,
            allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
            allow_headers=[
                "mcp-protocol-version",
                "mcp-session-id",
                "Authorization",
                "Content-Type",
            ],
            expose_headers=["mcp-session-id"],
        )
    ]

    # Create the HTTP app with CORS middleware
    app = mcp.http_app(middleware=middleware)

    # Run with uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
    )