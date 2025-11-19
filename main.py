import asyncio

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner

from agent.planner.function import manager_agent
from utils.config import final_text_from_response

load_dotenv()


async def main():
    # Simulate the dynamic context (reading from your files)

    runner = InMemoryRunner(agent=manager_agent)

    print("🤖 Manager is thinking...")
    response = await runner.run_debug(
        "Please plan my meal, Today, I want something high in protein."
    )
    final_text = await final_text_from_response(response)
    print(final_text)


if __name__ == "__main__":
    asyncio.run(main())
