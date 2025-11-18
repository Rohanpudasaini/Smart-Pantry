from google.adk.runners import InMemoryRunner

from agent.macros.functions import nutritionist_agent
from utils.config import final_text_from_response


async def main():
    runner = InMemoryRunner(agent=nutritionist_agent)
    response = await runner.run_debug("Calculate macros for 'Chicken Breast'.")
    print(await final_text_from_response(response))
