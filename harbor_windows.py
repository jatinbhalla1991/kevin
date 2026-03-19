"""
Windows-compatible Harbor runner that sets the correct event loop policy.
"""
import asyncio
import sys
import os

# Set the Windows ProactorEventLoop policy to support subprocess operations
if sys.platform == 'win32':
    # Use WindowsProactorEventLoopPolicy which supports subprocess on Windows
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    # Also ensure any existing loop is closed
    try:
        loop = asyncio.get_event_loop()
        if not loop.is_closed():
            loop.close()
    except RuntimeError:
        pass
    # Create a new event loop with Proactor
    asyncio.set_event_loop(asyncio.ProactorEventLoop())

# Now import and run Harbor
from harbor.cli.main import main

if __name__ == "__main__":
    main()
