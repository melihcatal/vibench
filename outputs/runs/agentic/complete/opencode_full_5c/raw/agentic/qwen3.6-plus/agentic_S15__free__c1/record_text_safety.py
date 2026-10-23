import os
import json
from openai import OpenAI
from database_models import TextSafetyRequest, TextSafetyResponse

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"

DEFAULT_CATEGORIES = [
    "hate",
    "self-harm",
    "sexual",
    "violence",
    "harassment",
    "illegal",
]


def check_text_safety(request: TextSafetyRequest) -> TextSafetyResponse:
    client = OpenAI(api_key=OPENAI_API_KEY)

    categories = request.categories or DEFAULT_CATEGORIES
    combined_text = "\n".join(f"{k}: {v}" for k, v in request.fields_to_check.items())

    system_prompt = (
        "You are a content safety moderation assistant. "
        "Review the provided text fields and determine whether they contain unsafe content. "
        f"Check specifically for these categories: {', '.join(categories)}. "
        "Return your analysis as a JSON object with the following structure:\n"
        '{"is_safe": true/false, "flags": [{"category": "...", "field": "...", "severity": "low|medium|high", "reason": "..."}]}\n'
        'If no unsafe content is found, return {"is_safe": true, "flags": []}.'
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": combined_text},
        ],
        temperature=0.0,
        max_tokens=500,
        response_format={"type": "json_object"},
    )

    result_json = json.loads(response.choices[0].message.content.strip())

    flags = result_json.get("flags", [])
    is_safe = result_json.get("is_safe", True)

    return TextSafetyResponse(
        document_id=request.document_id,
        is_safe=is_safe,
        flags=flags,
        model_used=OPENAI_MODEL,
    )


def check_text_safety_raw(
    document_id: str, fields_to_check: dict, categories: list = None
) -> dict:
    request = TextSafetyRequest(
        document_id=document_id,
        fields_to_check=fields_to_check,
        categories=categories,
    )
    response = check_text_safety(request)
    return response.to_dict()


if __name__ == "__main__":
    result = check_text_safety_raw(
        document_id="doc-002",
        fields_to_check={
            "comment": "This is a perfectly normal and safe comment.",
            "description": "A helpful product description for our store.",
        },
    )
    print(json.dumps(result, indent=2))
