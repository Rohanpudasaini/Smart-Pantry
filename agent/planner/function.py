from google.adk import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner

from agent.macros.functions import nutritionist_agent
from agent.recipe.functions import chef_agent
from utils.config import final_text_from_response


async def run_runner(agent: Agent, request: str):
    """
    Runs the agent and returns the final answer.
    Priority: 1. Model's text explanation. 2. The raw tool output (if model is silent).
    """
    runner = InMemoryRunner(agent=agent)
    response = await runner.run_debug(request)

    return await final_text_from_response(response)


async def ask_chef(request: str):
    """Use this tool to ask the Chef Agent for recipe ideas."""
    # In ADK, we often use .chat() or .run() depending on the version
    return await run_runner(chef_agent, request)

    # response = chef_agent.chat(request)
    # return response.content


async def ask_nutritionist(request: str):
    """Use this tool to ask the Nutritionist Agent for macro data."""
    return await run_runner(nutritionist_agent, request)


def save_plan_file(content: str):
    """Saves the final text to a file."""
    with open("todays_meal_plan.md", "w") as f:
        f.write(content)
    return "Plan saved."


# 3. ORCHESTRATOR: The Manager Agent
# ---------------------------------------------------------

manager_agent = Agent(
    name="manager_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite"
    ),  # Stronger model for the manager is better
    description="The head meal planner.",
    instruction="""
    You are the Manager of the Smart Pantry.
    
    YOUR GOAL: Create a verified meal plan for the user.
    
    PROCESS:
    1. Read the context (Pantry/Goal) provided by the user.
    2. Call `ask_chef` to get recipe ideas using the pantry items.
    3. Pick the best recipe and call `ask_nutritionist` to verify its protein content.
    4. If it fits the goal, write the final plan using `save_plan_file`.
    """,
    # The Manager's tools are the FUNCTIONS that trigger the other agents
    tools=[ask_chef, ask_nutritionist, save_plan_file],
)
