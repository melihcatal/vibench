import os
from openai import OpenAI

from model_client import build_messages, get_model_name
from model_models import safe_json_loads

EXTRACT_MODEL = get_model_name(os.getenv("EXTRACT_MODEL", "gpt-4.1-mini"))


def extract_json(text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))
    response = client.chat.completions.create(
        model=EXTRACT_MODEL,
        messages=build_messages(
            "You extract structured JSON from text using hosted OpenAI chat completions.",
            "Return only valid JSON with keys: entities, dates, actions, and summary.\n\nText:\n" + text,
        ),
        temperature=0.0,
        response_format={"type": "json_object"},
    )
    return safe_json_loads(response.choices[0].message.content or "{}")
