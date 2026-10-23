import openai
import os
from database_models import Document


def check_user_generated_document_fields_for_unsafe_content(
    document: Document,
) -> dict[str, bool]:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    results: dict[str, bool] = {}
    for field, value in document.items():
        if isinstance(value, str) and value.strip():
            response = client.moderations.create(input=value)
            results[field] = not response.results[0].flagged
        else:
            results[field] = True
    return results
