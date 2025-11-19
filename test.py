# import asyncio

# from dotenv import load_dotenv

# from agent.macros.test import main

# if __name__ == "__main__":
#     load_dotenv()
#     asyncio.run(main())

from agent.file_handeling.functions import get_meal_history, get_pantry_items
print(get_meal_history())
print(get_pantry_items())