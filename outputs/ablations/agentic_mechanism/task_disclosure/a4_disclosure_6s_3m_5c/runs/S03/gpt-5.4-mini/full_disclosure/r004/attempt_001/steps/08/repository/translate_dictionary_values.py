import os
from typing import Any, Dict, Optional

from openai import OpenAI


def _translate_value(client: OpenAI, value: Any, source_language: str, target_language: str, model: str) -> Any:
    if isinstance(value, str):
        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a translation engine. Translate the user's text from "
                        f"{source_language} to {target_language}. Return only the translated text."
                    ),
                },
                {"role": "user", "content": value},
            ],
        )
        return response.output_text.strip()
    if isinstance(value, dict):
        return {key: _translate_value(client, nested_value, source_language, target_language, model) for key, nested_value in value.items()}
    if isinstance(value, list):
        return [_translate_value(client, item, source_language, target_language, model) for item in value]
    return value


def translate_dictionary_values(values: Dict[str, Any], source_language: str, target_language: str, model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    chosen_model = model or "gpt-5.4-mini"
    return {key: _translate_value(client, value, source_language, target_language, chosen_model) for key, value in values.items()}
