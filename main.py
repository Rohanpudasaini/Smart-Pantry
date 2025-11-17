import asyncio

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner

from agent.planner.function import manager_agent
from utils.config import final_text_from_response

load_dotenv()


async def main():
    # Simulate the dynamic context (reading from your files)
    user_pantry = "Chicken Breast, Rice, Spinach"
    user_goal = "High protein dinner (40g+)"

    runner = InMemoryRunner(agent=manager_agent)

    print("🤖 Manager is thinking...")
    response = await runner.run_debug(
        f"Context: Pantry=[{user_pantry}], Goal=[{user_goal}]. Please plan my meal."
    )
    final_text = await final_text_from_response(response)
    print(final_text)


if __name__ == "__main__":
    asyncio.run(main())
