# Copyright (c) 2025 devgagan : https://github.com/devgaganin.
# Licensed under the GNU General Public License v3.0.
# See LICENSE file in the repository root for full license text.

import asyncio
import importlib
import os
import sys
from shared_client import start_client

async def load_and_run_plugins():
    """Loads and runs plugins dynamically."""
    await start_client()
    plugin_dir = "plugins"

    # Ensure the plugins directory exists
    if not os.path.exists(plugin_dir):
        print(f"Error: Plugin directory '{plugin_dir}' not found.")
        return
    
    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        try:
            module = importlib.import_module(f"plugins.{plugin}")
            if hasattr(module, f"run_{plugin}_plugin"):
                print(f"Running {plugin} plugin...")
                await getattr(module, f"run_{plugin}_plugin")()
        except Exception as e:
            print(f"Error loading {plugin}: {e}")

async def main():
    """Main loop to keep the script running."""
    await load_and_run_plugins()
    while True:
        await asyncio.sleep(1)  # Keeps the script alive

if __name__ == "__main__":
    print("Starting clients ...")
    try:
        asyncio.run(main())  # Modern way to run async main
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
