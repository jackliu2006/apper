import asyncio
from fastmcp import Client

# HTTP server
client = Client("http://127.0.0.1:8000/mcp/")


async def main():
    async with client:
        tools = await client.list_tools()
        # tools -> list[mcp.types.Tool]

        for tool in tools:
            print(f"Tool: {tool.name}")
            print(f"Description: {tool.description}")
            if tool.inputSchema:
                print(f"Parameters: {tool.inputSchema}")
            # Access tags and other metadata
            if hasattr(tool, 'meta') and tool.meta:
                fastmcp_meta = tool.meta.get('_fastmcp', {})
                print(f"Tags: {fastmcp_meta.get('tags', [])}")


asyncio.run(main())
