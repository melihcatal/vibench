import os
import json
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


def check_text_safety(text: str) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )

    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": {
            "sexual": result.categories.sexual,
            "hate": result.categories.hate,
            "harassment": result.categories.harassment,
            "self_harm": result.categories.self_harm,
            "sexual_minors": result.categories.sexual_minors,
            "hate_threatening": result.categories.hate_threatening,
            "violence_graphic": result.categories.violence_graphic,
            "self_harm_intent": result.categories.self_harm_intent,
            "self_harm_instructions": result.categories.self_harm_instructions,
            "harassment_threatening": result.categories.harassment_threatening,
            "violence": result.categories.violence,
        },
        "category_scores": {
            "sexual": result.category_scores.sexual,
            "hate": result.category_scores.hate,
            "harassment": result.category_scores.harassment,
            "self_harm": result.category_scores.self_harm,
            "sexual_minors": result.category_scores.sexual_minors,
            "hate_threatening": result.category_scores.hate_threatening,
            "violence_graphic": result.category_scores.violence_graphic,
            "self_harm_intent": result.category_scores.self_harm_intent,
            "self_harm_instructions": result.category_scores.self_harm_instructions,
            "harassment_threatening": result.category_scores.harassment_threatening,
            "violence": result.category_scores.violence,
        },
    }


def check_document_safety(document: dict, text_fields: list = None) -> dict:
    if hasattr(document, "to_dict"):
        doc_data = document.to_dict()
    else:
        doc_data = document

    data = doc_data.get("data", doc_data)
    if isinstance(data, str):
        data = json.loads(data)

    if text_fields is None:
        text_fields = [k for k, v in data.items() if isinstance(v, str)]

    results = {}
    overall_flagged = False

    for field in text_fields:
        value = data.get(field, "")
        if value:
            safety_result = check_text_safety(value)
            results[field] = safety_result
            if safety_result["flagged"]:
                overall_flagged = True

    return {
        "document_id": doc_data.get("document_id", ""),
        "overall_flagged": overall_flagged,
        "field_results": results,
    }
