import json
import os

from google import genai

from model_client import default_config
from model_models import json_hint, normalize_text


def extract_json(text: str, schema: dict | None = None) -> dict:
    config = default_config()
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    prompt = f"Extract structured data from the text. {json_hint(schema)}\n\nText:\n{normalize_text(text)}"
    response = client.models.generate_content(model=config.model, contents=prompt)
    return json.loads(response.text or "{}")
