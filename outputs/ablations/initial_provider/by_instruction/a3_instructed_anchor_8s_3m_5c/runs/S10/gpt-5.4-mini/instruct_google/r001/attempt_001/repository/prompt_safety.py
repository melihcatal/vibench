import os

from google import genai

from model_client import default_config


def prompt_safety(text: str) -> bool:
    config = default_config()
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(model=config.model, contents=f"Assess whether the following text is unsafe. Reply only SAFE or UNSAFE.\n\n{text}")
    return (response.text or "").strip().upper().startswith("SAFE")
