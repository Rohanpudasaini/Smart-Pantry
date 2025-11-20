import argparse
import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent.planner.function import manager_agent

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
    if not message:
        raise ValueError(
            "Please provide a message using --message or as a positional argument."
        )
    return message


async def main():
    message = await parse_arguments()
    app_name, user_id, session_id = "agents", "user1", "session1"
    session_service = InMemorySessionService()
    _ = await session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )
    runner = Runner(
        agent=manager_agent, app_name=app_name, session_service=session_service
    )

    prompt = types.Content(
        role="user",
        parts=[types.Part(text=str(message))],
    )
    full_response_text = ""
    final_text = ""
    for event in runner.run(user_id=user_id, session_id=session_id, new_message=prompt):
        if (
            event.partial
            and event.content
            and event.content.parts
            and event.content.parts[0].text
        ):
            full_response_text += event.content.parts[0].text
        if event.is_final_response:
            # if not event.partial and event.content and event.content.parts:
            final_text += full_response_text + (
                event.content.parts[0].text if event.content.parts[0].text else ""  # type: ignore
            )
            print(final_text.strip())
    return final_text.strip()


if __name__ == "__main__":
    asyncio.run(main())
