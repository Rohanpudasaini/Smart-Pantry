import json
import os


def get_pantry_items() -> str:
    """Reads the pantry.txt file and returns the ingredients."""
    file_path = "templates/pantry.txt"
    if not os.path.exists(file_path):
        return "Pantry file not found."

    with open(file_path, "r") as f:
        items = f.readlines()
    items = [item.strip() for item in items if item.strip()]
    if not items:
        return "Pantry is empty."
    return ", ".join(items)


def get_meal_history() -> str:
    """Reads meal_log.json and returns past meals."""

    file_path = "templates/meal_log.json"
    limit = 3
    if not os.path.exists(file_path):
        return "No past meals found."

    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        # 2. Safety Check: Is it a list?
        if not isinstance(data, list):
            return "Error: Log file is not a valid list."

        # 3. The Magic Slice: Get last 'limit' items
        # If list has 1 item, data[-3:] correctly returns just that 1 item.
        last_entries = data[-limit:]

        # 4. Extract just the names (to save token space in your prompt)
        # We use .get() to avoid crashing if "recipe" key is missing
        meal_names = [item.get("recipe", "Unknown Meal") for item in last_entries]

        return ", ".join(meal_names)

    except json.JSONDecodeError:
        return "Error: Log file is corrupted."
