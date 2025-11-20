import os

import httpx
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.models.google_llm import Gemini

load_dotenv()
API_KEY = os.getenv("RECIPE_API_KEY")
if not API_KEY:
    raise ValueError("RECIPE_API_KEY not found in environment variables.")

API_BASE_URL = "https://api.spoonacular.com/recipes/findByIngredients"


def search_recipes_tool(ingredients: str):
    """Searches for recipes based on ingredients."""
    print("Searching recipes for ingredients:", ingredients)
    params = {
        "ingredients": ingredients,
        "number": 3,
        "apiKey": API_KEY,
    }
    with httpx.Client() as client:
        response = client.get(API_BASE_URL, params=params)
        # response.raise_for_status()
        data = response.json()
    recipe_names = [recipe["title"] for recipe in data]
    print("Found recipes:", recipe_names)
    return f"Found recipes: {', '.join(recipe_names)}"


chef_agent = Agent(
    name="chef_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),  # Use the model you have access to
    description="A creative chef who finds recipes.",
    instruction="You are a creative chef. Given a list of ingredients, find recipe that can be made using those ingredients.",
    tools=[search_recipes_tool],
)
