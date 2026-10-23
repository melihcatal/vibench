from __future__ import annotations

from messaging_client import get_openai_client, get_openai_model
from messaging_models import extract_text


def translate_payload_text(
    payload: dict, target_language: str, field_name: str = "text"
) -> dict:
    client = get_openai_client()
    model = get_openai_model("gpt-4.1-mini")
    source_text = extract_text(payload, field_name=field_name)
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Translate customer-facing text to {target_language}. Return only the translation.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": source_text}],
            },
        ],
    )
    translated = dict(payload)
    translated[field_name] = response.output_text.strip()
    translated["translated_to"] = target_language
    translated["translation_model"] = model
    return translated
