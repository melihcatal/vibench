from typing import Any, Dict

from openai import OpenAI

from database_models import normalize_text_fields


def record_translate(
    document: Dict[str, Any], field_names: list[str], target_language: str
) -> Dict[str, Any]:
    fields = normalize_text_fields(document, field_names)
    client = OpenAI(api_key=__import__("os").getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate each field value into {target_language}. Return strict JSON object only.",
            },
            {
                "role": "user",
                "content": str(fields),
            },
        ],
    )
    return {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "targetLanguage": target_language,
        "translation": response.output_text,
    }
