from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

NUTRIENT_IDS = {1003: "Protein", 1004: "Fat", 1005: "Carbs"}


async def final_text_from_response(response):
    final_text = ""
    last_tool_output = ""

    for event in response:
        if not event.content:
            continue

        # CHECK 1: Did the Model speak?
        if event.content.role == "model" and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    final_text += part.text

        # CHECK 2: Did a Tool return a result? (Fallback)
        # In ADK, the tool output usually comes in an event with role='user' or 'function'
        if event.content.parts:
            for part in event.content.parts:
                if part.function_response:
                    # We found a tool response! Let's save it just in case.
                    # The actual data is usually in a dictionary called 'response'
                    resp_dict = part.function_response.response

                    # Extract the string. Usually key is 'result' or 'message'
                    if "result" in resp_dict:
                        last_tool_output = str(resp_dict["result"])
                    elif "message" in resp_dict:
                        last_tool_output = str(resp_dict["message"])
                    else:
                        # Fallback: just grab the whole dict as a string
                        last_tool_output = str(resp_dict)

    # DECISION TIME:
    # If the model wrote a summary (final_text), return that.
    # If the model stayed silent (like in your log), return the tool's raw output.
    if final_text.strip():
        return final_text
    else:
        return last_tool_output
    # final_text = ""

    # for event in response:
    #     # FIX 1: Check if content exists first
    #     if not event.content:
    #         continue

    #     # FIX 2: 'role' is inside 'content', not 'event'
    #     if event.content.role == "model":
    #         for part in event.content.parts:  # type: ignore
    #             # We only want the text parts (ignoring function_calls)
    #             if part.text:
    #                 final_text += part.text
    # return final_text
