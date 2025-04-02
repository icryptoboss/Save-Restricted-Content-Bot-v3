import asyncio
import importlib
import os
import sys
import time
from telethon.errors import FloodWaitError  # Import FloodWaitError
from shared_client import start_client

async def load_and_run_plugins():
    await start_client()
    plugin_dir = "plugins"
    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        module = importlib.import_module(f"plugins.{plugin}")
        if hasattr(module, f"run_{plugin}_plugin"):
            print(f"Running {plugin} plugin...")
            await getattr(module, f"run_{plugin}_plugin")()  

async def main():
    try:
        await load_and_run_plugins()
        while True:
            await asyncio.sleep(1)
    except FloodWaitError as e:
        wait_time = e.seconds
        print(f"Rate limited! Waiting {wait_time} seconds before retrying...", file=sys.stderr)
        time.sleep(wait_time)  # Sleep for the required duration
        await main()  # Restart the bot after waiting
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    print("Starting clients ...")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        try:
            loop.close()
        except Exception:
            pass
