from model_client import select_model_for_task, get_api_key
from model_models import build_prompt_for_extract_json
from openai import OpenAI
import json


def extract_json(text: str) -> dict:
    provider, model = select_model_for_task("extract_json")
    api_key = get_api_key(provider)
    client = OpenAI(api_key=api_key)
    messages = build_prompt_for_extract_json(text)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.0,
        max_tokens=2048,
    )
    content = response.choices[0].message.content.strip()
    return json.loads(content)
