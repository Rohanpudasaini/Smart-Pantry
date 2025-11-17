def get_pantry_items() -> str:
    """Reads the pantry.txt file and returns the ingredients."""
    # Your FileHandling logic here
    return "Chicken Breast, Rice, Eggs, Spinach"


def get_meal_history() -> str:
    """Reads meal_log.json and returns past meals."""
    # Your FileHandling logic here
    return "Yesterday: Chicken Curry. Day before: Egg Salad."


def save_plan_tool(content: str):
    """Writes the final plan to todays_meal_plan.md"""
    with open("todays_meal_plan.md", "w") as f:
        f.write(content)
    return "Plan saved successfully."
