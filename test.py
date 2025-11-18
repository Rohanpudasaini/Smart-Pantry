import asyncio

from dotenv import load_dotenv

from agent.macros.test import main

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
