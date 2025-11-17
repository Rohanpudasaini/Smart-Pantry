from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini


async def get_macros_tool(food_item: str):
    """Calculates macros for a food item."""
    # [INSERT YOUR USDA API CODE HERE]
    return {"message": f"Macros for {food_item}: 30g Protein, 10g Fat."}


nutritionist_agent = Agent(
    name="nutritionist_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    description="A strict nutritionist who calculates data.",
    instruction="You are a nutritionist. Output ONLY the macros for the requested food.",
    tools=[get_macros_tool],
)
