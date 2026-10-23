import os
from openai import OpenAI
from database_models import DocumentResponse, SafetyCheckResult

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def check_text_safety(
    documents: list[DocumentResponse], fields: list[str] = None
) -> list[SafetyCheckResult]:
    client = OpenAI(api_key=OPENAI_API_KEY)
    results = []

    for doc in documents:
        fields_to_check = fields or list(doc.data.keys())
        for field_name in fields_to_check:
            field_value = doc.data.get(field_name, "")
            if not isinstance(field_value, str):
                field_value = str(field_value)
            if not field_value.strip():
                continue

            response = client.moderations.create(
                model="text-moderation-latest",
                input=field_value,
            )

            result_obj = response.results[0]
            categories = result_obj.categories.model_dump()
            scores = result_obj.category_scores.model_dump()
            flags = [cat for cat, flagged in categories.items() if flagged]
            max_score = max(scores.values()) if scores else 0.0

            results.append(
                SafetyCheckResult(
                    document_id=doc.document_id,
                    field_name=field_name,
                    is_safe=len(flags) == 0,
                    flags=flags,
                    confidence=1.0 - max_score,
                )
            )

    return results
