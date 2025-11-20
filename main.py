import argparse
import asyncio

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner

from agent.planner.function import manager_agent
from utils.config import final_text_from_response

load_dotenv()


async def parse_arguments():
    parser = argparse.ArgumentParser(description="Simple Gemini AI Agent")
    parser.add_argument(
        "positional_message", nargs="?", help="Message to send to the AI"
    )

    parser.add_argument(
        "--message", "-m", type=str, help="The message to send to the Gemini AI model"
    )

    args = parser.parse_args()
    message = args.message or args.positional_message
    return message


async def main():
    # Simulate the dynamic context (reading from your files)
    default_message = "Please plan my meal, Today, I want something high in protein."
    message = await parse_arguments() or default_message

    runner = InMemoryRunner(agent=manager_agent)

    print("🤖 Manager is thinking...")
    response = await runner.run_debug(message)
    final_text = await final_text_from_response(response)
    print(final_text)


if __name__ == "__main__":
    asyncio.run(main())
