from typing import Any, Dict

from openai import OpenAI

from database_models import normalize_text_fields


def record_text_safety(
    document: Dict[str, Any], field_names: list[str]
) -> Dict[str, Any]:
    fields = normalize_text_fields(document, field_names)
    client = OpenAI(api_key=__import__("os").getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        model="omni-moderation-latest", input=list(fields.values())
    )
    flagged = any(result.flagged for result in response.results)
    return {
        "provider": "openai",
        "model": "omni-moderation-latest",
        "flagged": flagged,
        "fields": list(fields.keys()),
        "results": [result.model_dump() for result in response.results],
    }
