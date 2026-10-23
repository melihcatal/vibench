from document_client import get_openai_client, default_model
from document_models import build_normalization_payload, coerce_json_response


def normalize_expense(extracted_fields: dict):
    client = get_openai_client()
    payload = build_normalization_payload(extracted_fields)
    response = client.responses.create(
        model=default_model(),
        input=[
            {"role": "system", "content": "Normalize expense data into a standard JSON schema."},
            {"role": "user", "content": payload},
        ],
        response_format={"type": "json_object"},
    )
    return coerce_json_response(response)
