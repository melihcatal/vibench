import os
from typing import Any, Dict

from openai import OpenAI


def _translate_text(client: OpenAI, text: str, target_language: str) -> str:
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Translate the user's text into the target language. Return only the translation.",
            },
            {
                "role": "user",
                "content": f"Target language: {target_language}\nText: {text}",
            },
        ],
    )
    return response.output_text.strip()


def translate_dictionary_values(data: Dict[str, Any], target_language: str = "Spanish") -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def translate_value(value: Any) -> Any:
        if isinstance(value, dict):
            return {k: translate_value(v) for k, v in value.items()}
        if isinstance(value, list):
            return [translate_value(item) for item in value]
        if isinstance(value, str):
            return _translate_text(client, value, target_language)
        return value

    return {key: translate_value(value) for key, value in data.items()}
