"""Entry point for running Zentao MCP Server"""
import asyncio
import sys
from .server import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.", file=sys.stderr)
        sys.exit(0)
