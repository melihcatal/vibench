import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Assumes OPENAI_API_KEY is set in the environment
try:
    client = OpenAI()
except Exception as e:
    print(f"Could not initialize OpenAI client: {e}")
    client = None

def moderate_profile_text(text: str) -> dict:
    """
    Moderates user-provided profile text using OpenAI's Moderation API.
    """
    if not client:
        raise ConnectionError("OpenAI client not initialized.")
    if not text.strip():
        return {"flagged": False, "categories": {}}

    response = client.moderations.create(input=text, model="text-moderation-stable")
    result = response.results[0]

    flagged_categories = {cat: val for cat, val in result.categories.model_dump().items() if val}

    return {
        "flagged": result.flagged,
        "categories": flagged_categories,
    }
