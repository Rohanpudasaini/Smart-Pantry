from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)


async def final_text_from_response(response):
    final_text = ""

    for event in response:
        # FIX 1: Check if content exists first
        if not event.content:
            continue

        # FIX 2: 'role' is inside 'content', not 'event'
        if event.content.role == "model":
            for part in event.content.parts:  # type: ignore
                # We only want the text parts (ignoring function_calls)
                if part.text:
                    final_text += part.text
    return final_text
