from google.adk import Agent
from google.adk.models.google_llm import Gemini


def search_recipes_tool(ingredients: str):
    """Searches for recipes based on ingredients."""
    # [INSERT YOUR SPOONACULAR API CODE HERE]
    return {
        "message": f"Found recipes for {ingredients}: 'Lemon Chicken', 'Rice Bowl'."
    }


chef_agent = Agent(
    name="chef_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),  # Use the model you have access to
    description="A creative chef who finds recipes.",
    instruction="You are a creative chef. Given a list of ingredients, find recipe names.",
    tools=[search_recipes_tool],
)
