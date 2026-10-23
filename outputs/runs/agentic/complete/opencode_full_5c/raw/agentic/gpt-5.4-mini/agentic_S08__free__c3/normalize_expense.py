import json

from document_client import get_client, get_model
from document_models import standard_expense_schema


def normalize_expense(extracted: dict):
    client = get_client()
    resp = client.responses.create(
        model=get_model(),
        input=f"Normalize this extracted expense into a standard JSON schema: {json.dumps(extracted)}",
    )
    data = json.loads(resp.output_text)
    return standard_expense_schema(data)
