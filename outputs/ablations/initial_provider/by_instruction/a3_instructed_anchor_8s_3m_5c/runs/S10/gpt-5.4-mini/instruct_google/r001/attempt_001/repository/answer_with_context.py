import os

from google import genai

from model_client import default_config
from model_models import normalize_text


def answer_with_context(question: str, context: str) -> str:
    config = default_config()
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    prompt = f"Use the context to answer the question accurately.\n\nContext:\n{normalize_text(context)}\n\nQuestion:\n{normalize_text(question)}"
    response = client.models.generate_content(model=config.model, contents=prompt)
    return response.text or ""
