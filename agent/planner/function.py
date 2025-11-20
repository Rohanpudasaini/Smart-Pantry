import datetime
import json

from google.adk import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent.file_handeling.functions import get_meal_history, get_pantry_items
from agent.macros.functions import nutritionist_agent
from agent.recipe.functions import chef_agent


async def run_runner(agent: Agent, request: str):
    """
    Runs the agent and returns the final answer.
    Priority: 1. Model's text explanation. 2. The raw tool output (if model is silent).
    """
    app_name, user_id, session_id = "agents", "user1", "session1"
    session_service = InMemorySessionService()
    runner = Runner(agent=agent, app_name=app_name, session_service=session_service)
    _ = await session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )

    message = types.Content(
        role="user",
        parts=[types.Part(text=request)],
    )
    full_response_text = ""
    final_text = ""
    for event in runner.run(
        user_id=user_id, session_id=session_id, new_message=message
    ):
        if (
            event.partial
            and event.content
            and event.content.parts
            and event.content.parts[0].text
        ):
            full_response_text += event.content.parts[0].text
        if event.is_final_response:
            final_text = full_response_text + str(
                event.content.parts[0].text if not event.partial else ""  # type: ignore
            )
            print(final_text.strip())
    return final_text.strip()


async def ask_chef(request: str):
    """Use this tool to ask the Chef Agent for recipe ideas.
    The tool takes a request string containing pantry items separated by commas,
    and returns recipe ideas which have those pantry items.
    args:
        request (str): The request string containing pantry items separated by commas.
    returns:
        str: The recipe ideas from the Chef Agent.
    """
    return await run_runner(chef_agent, request)


async def ask_nutritionist(request: str):
    """Use this tool to ask the Nutritionist Agent for macro data.
    args:
        request (str): The request string containing name of the food item.
    returns:
        str: The macro data from the Nutritionist Agent.
        example:
        Found 'Chicken': Protein: 21.58g, Fat: 29.84g, Carbs: 0.12g
    """
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
    6. Always write the final plan using `save_plan_file`.
    7. If there are more than one recipe ideas, pick any one and **always** save the final plan using `save_plan_file`.
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
