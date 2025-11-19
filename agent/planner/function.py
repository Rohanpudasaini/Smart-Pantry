import datetime
import json

from google.adk import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner

from agent.file_handeling.functions import get_meal_history, get_pantry_items
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
    """Saves the final markdown to a file.
    Args:
        content (str): The markdown content to save.
        format:
            "
                ## Meal Plan:

                ### Today:
                **Bbq Chicken and Goat Cheese Ravioli**
                *   **Protein:** 21.58g
                *   **Fat:** 29.84g
                *   **Carbs:** 0.12g
    Returns:
        str: Confirmation message.
    """
    with open("templates/todays_meal_plan.md", "w") as f:
        f.write(content)

    with open("templates/meal_log.json", "r") as f:
        meal_log = json.load(f)

    # Append the new plan to the meal log
    new_entry = {
        "date": datetime.date.today().isoformat(),  # You might want to dynamically set this date
        "recipe": content.split("\n")[3].strip(
            "**"
        ),  # Extract recipe name from content
    }
    meal_log.append(new_entry)

    with open("templates/meal_log.json", "w") as f:
        json.dump(meal_log, f, indent=2)

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
    
    YOUR GOAL: Create a verified meal plan for the user, always use the available tools and never give answer by yourself.
    your goal is to always provide a meal plan so act only as a planner and orchestrator of other agents.
    Don't ask for more information from the user, use the tools to get all needed data.
    After getting recipe and macros, *ALWAYS* save the final plan using `save_plan_file` tool.
    
    PROCESS:
    1. Read the context (Pantry/Goal) provided by the user.
    2. Use `get_pantry_items` to list available ingredients.
    3. Use `get_meal_history` to understand past meals.
    4. Call `ask_chef` to get recipe ideas using the pantry items.
    5. Pick the best recipe and call `ask_nutritionist` and ensure same recipe isn't repeated.
    6. If it fits the goal, write the final plan using `save_plan_file`.
    """,
    # The Manager's tools are the FUNCTIONS that trigger the other agents
    tools=[
        ask_chef,
        ask_nutritionist,
        save_plan_file,
        get_pantry_items,
        get_meal_history,
    ],
)
