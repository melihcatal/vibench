import os

from google import genai

from model_client import default_config


def result_translate(text: str, target_language: str) -> str:
    config = default_config()
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(model=config.model, contents=f"Translate to {target_language}:\n\n{text}")
    return response.text or ""
