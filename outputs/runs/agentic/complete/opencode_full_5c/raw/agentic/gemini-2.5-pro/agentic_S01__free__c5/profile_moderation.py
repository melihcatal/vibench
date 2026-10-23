import os
from openai import OpenAI


def moderate_profile_text(text: str) -> dict:
    """
    Moderates profile text using the OpenAI Moderation API.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.moderations.create(model="text-moderation-latest", input=text)
        return response.results[0].model_dump()
    except Exception as e:
        # Handle API errors or other exceptions
        print(f"An error occurred: {e}")
        return {"error": str(e)}
