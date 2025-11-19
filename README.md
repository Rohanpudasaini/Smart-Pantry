# 🤖 Smart Pantry - AI Nutrition Agent

This is a capstone project for the 5-Day AI Agents Intensive Course. It's a "Concierge Agent" designed to act as a personal nutritionist and chef, solving the problem of "what should I eat?"

The agent's goal is to plan daily meals based on three factors:
1.  **User Goals:** (e.g., hit 150g protein)
2.  **User Pantry:** (e.g., only use ingredients I have)
3.  **User History:** (e.g., don't suggest the same meal I ate yesterday)

---

## Core Features

* **Pantry-Aware Planning:** Only suggests recipes you can *actually* make with your available ingredients.
* **Goal-Oriented:** Builds a meal plan specifically to hit macro targets (like protein).
* **Variety Engine (Memory):** Remembers what you've eaten and actively suggests different meals to avoid boredom.
* **Multi-Tool Coordination:** Uses the *best* tool for each job (Spoonacular for recipes, USDA for macros).
* **File-Based Memory:** Uses a custom `FileHandlingAgent` to read/write from simple `.txt` and `.json` files, acting as the agent's persistent memory.

---

## 🧠 Agent Architecture

This project is a **multi-agent system** with one "Orchestrator" (the manager) and several "Tools" (the workers).

* **Orchestrator:** The main `main.py` script. It contains the core logic and decides which tool to call in what order.
* **Tools:**
    1.  **`FileHandlingAgent` (Custom Tool):** Our agent for managing state. It's responsible for:
        * `READ` from `pantry.txt`, `goals.json`, and `meal_log.json`.
        * `WRITE` the final `todays_meal_plan.md`.
        * `APPEND` to `meal_log.json` to update its memory.
    2.  **`SpoonacularAgent` (API Tool):** Finds recipe ideas by searching with a list of ingredients.
    3.  **`USDANutritionAgent` (API Tool):** Gets highly-accurate macronutrient data for specific ingredients.
    4.  **`LLM-PlannerAgent` (API Tool):** The "brain." It analyzes data, makes decisions, and writes the final human-readable plan.

---

## 🗺️ Project Roadmap

Follow these steps to build the project. Check them off as you go!

### Phase 1: Setup & Tool Building
- [ ] Initialize the project (`git init`, create `main.py`).
- [ ] Get API keys for **Spoonacular** and **USDA FoodData Central**.
- [ ] Create the three "memory" files:
    - [ ] `pantry.txt` (e.g., "chicken breast, eggs, rice, broccoli")
    - [ ] `goals.json` (e.g., `{"protein_target": 150, "dislikes": "fish"}`)
    - [ ] `meal_log.json` (e.g., `[]` - an empty list to start)
- [ ] Build your **`FileHandlingAgent`** with `read(path)`, `write(path, content)`, and `append(path, content)` functions.
- [ ] Create the **`SpoonacularAgent`** tool (a function that takes ingredients and returns recipes).
- [ ] Create the **`USDANutritionAgent`** tool (a function that takes an ingredient and returns its macros).
- [ ] Create the **`LLM-PlannerAgent`** tool (a function that takes a prompt and returns a plan).

### Phase 2: Basic "Smart" Workflow
- [ ] Implement the core Orchestrator logic in `main.py`.
- [ ] **Step 1:** Use `FileHandlingAgent` to read `pantry.txt` and `goals.json`.
- [ ] **Step 2:** Use `SpoonacularAgent` to get a *list* of potential recipes.
- [ ] **Step 3:** Use `LLM-PlannerAgent` to *choose the best* recipe from the list (e.g., "pick the one that sounds highest in protein").
- [ ] **Step 4:** Use `SpoonacularAgent` again to get the *specific ingredients* for the *one* chosen recipe.
- [ ] **Step 5:** Use `USDANutritionAgent` in a loop to get the *exact macros* for each ingredient.
- [ ] **Step 6:** Use `LLM-PlannerAgent` (the main prompt) to assemble the final plan, calculate totals, and suggest snacks for remaining goals.
- [ ] **Step 7:** Use `FileHandlingAgent` to write the final output to `todays_meal_plan.md`.
- [ ] **Test:** Run the `main.py` and see if it generates a complete plan!

### Phase 3: Add Memory & Variety
- [ ] **Modify Step 1:** Use `FileHandlingAgent` to *also* read `meal_log.json`.
- [ ] **Modify Step 3/6:** Update the LLM prompts to include: "Here is the user's meal history: `[...log...]`. You **must** suggest a new recipe that is not on this list."
- [ ] **Step 8 (New):** After the plan is generated, use `FileHandlingAgent` to `append` the new meal (e.g., `{"date": "2025-11-16", "recipe": "Chicken Tacos"}`) to `meal_log.json`.


### Phase 4: Polish & Error Handling
- [ ] Add error handling for when `SpoonacularAgent` finds 0 recipes. (The agent should tell the user this).
- [ ] Add error handling for when `pantry.txt` is empty. (The agent should ask the user to fill it).
- [ ] Clean up the code and add comments.
- [ ] **Project Complete!** 🚀