import os

from google import genai

from model_client import default_config


def spoken_brief(text: str) -> str:
    config = default_config()
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(model=config.model, contents=f"Rewrite this as a short spoken brief:\n\n{text}")
    return response.text or ""
