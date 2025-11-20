import os

import httpx
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.models.google_llm import Gemini

from utils.config import NUTRIENT_IDS

load_dotenv()

API_KEY = os.getenv("USDA_API_KEY")
if not API_KEY:
    raise ValueError("USDA_API_KEY not found in environment variables.")


async def get_macros_tool(food_name: str):
    """Calculates macros for a food item."""
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "query": food_name,
        "pageSize": 1,
        "api_key": API_KEY,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code != 200:
        msg = f"Error: USDA API returned status {response.status_code}"
        print(msg)
        return msg

    data = response.json()

    # 1. Safety Check: Did we get any food back?
    if not data.get("foods"):
        msg = f"No food found for '{food_name}'."
        print(msg)
        return msg

    # 2. Get the first result
    food_item = data["foods"][0]
    description = food_item.get("description", "Unknown Food")

    # 3. Initialize macros with 0 default
    macros = {"Protein": 0.0, "Fat": 0.0, "Carbs": 0.0}

    # 4. Loop through the nutrients list to find our targets
    #    We use a loop because the order of nutrients is not guaranteed.
    for nutrient in food_item.get("foodNutrients", []):
        n_id = nutrient.get("nutrientId")

        if n_id in NUTRIENT_IDS:
            # Get the name (Protein/Fat/Carbs)
            name = NUTRIENT_IDS[n_id]
            # Get the value (default to 0 if missing)
            value = nutrient.get("value", 0.0)
            macros[name] = value

    # 5. Format the output string for the Agent
    return (
        f"Found '{description}': "
        f"Protein: {macros['Protein']}g, "
        f"Fat: {macros['Fat']}g, "
        f"Carbs: {macros['Carbs']}g"
    )


nutritionist_agent = Agent(
    name="nutritionist_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    description="A strict nutritionist who calculates data.",
    instruction="You are a nutritionist. Output ONLY the macros for the requested food.",
    tools=[get_macros_tool],
)
