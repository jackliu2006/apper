# Assumes the FastAPI app from above is already defined
from fastmcp import FastMCP
from fastapi import FastAPI
import os
from dotenv import load_dotenv
# Load .env file
load_dotenv("/Users/jackliu2006/workspace/apper/src/fastapi/.env")

from v1.routes import router as v1_router

app = FastAPI()

app.include_router(v1_router)

# 1. Generate MCP server from your API
mcp = FastMCP.from_fastapi(app=app, name="apper API MCP")

# 2. Create the MCP's ASGI app
mcp_app = mcp.http_app(path='/mcp')

# 3. Create a new FastAPI app that combines both sets of routes
app = FastAPI(
    title="Apper API with MCP",
    routes=[
        *mcp_app.routes,  # MCP routes
        *app.routes,      # Original API routes
    ],
    lifespan=mcp_app.lifespan,
)



# Now you have:
# - Regular API: http://localhost:8000/products
# - LLM-friendly MCP: http://localhost:8000/mcp/
# Both served from the same FastAPI application!

