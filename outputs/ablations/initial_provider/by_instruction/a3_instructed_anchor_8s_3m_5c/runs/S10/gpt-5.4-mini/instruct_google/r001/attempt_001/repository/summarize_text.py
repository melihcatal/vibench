import os

from google import genai

from model_client import default_config
from model_models import normalize_text


def summarize_text(text: str) -> str:
    config = default_config()
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    prompt = f"Summarize the following text concisely and faithfully:\n\n{normalize_text(text)}"
    response = client.models.generate_content(model=config.model, contents=prompt)
    return response.text or ""
