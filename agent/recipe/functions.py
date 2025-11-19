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
    try:
        with httpx.Client() as client:
            response = client.get(API_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
        if not isinstance(data, list):
            return "Error: Unexpected response format from recipe API."
        recipe_names = []
        for recipe in data:
            title = recipe.get("title")
            if title:
                recipe_names.append(title)
        if not recipe_names:
            return "No recipes found for the given ingredients."
        return f"Found recipes: {', '.join(recipe_names)}"
    except httpx.HTTPError as e:
        return f"Error: Failed to fetch recipes from API. {str(e)}"
    except Exception as e:
        return f"Error: An unexpected error occurred. {str(e)}"


chef_agent = Agent(
    name="chef_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),  # Use the model you have access to
    description="A creative chef who finds recipes.",
    instruction="You are a creative chef. Given a list of ingredients, find recipe that can be made using those ingredients.",
    tools=[search_recipes_tool],
)
