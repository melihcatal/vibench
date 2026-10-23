import os
from openai import OpenAI

def moderate_free_text_claim(text: str) -> dict:
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=openai_api_key)

    try:
        response = client.moderations.create(input=text)
        if response.results:
            return response.results[0].model_dump()
        return {"flagged": False, "categories": {}}
    except Exception as e:
        raise RuntimeError(f"Failed to moderate text with OpenAI: {e}")