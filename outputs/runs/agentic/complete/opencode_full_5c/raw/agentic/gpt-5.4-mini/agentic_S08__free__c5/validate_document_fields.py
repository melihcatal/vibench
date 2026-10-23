from document_client import get_openai_client, default_model
from document_models import build_validation_payload, coerce_json_response


def validate_document_fields(document_fields: dict):
    client = get_openai_client()
    payload = build_validation_payload(document_fields)
    response = client.responses.create(
        model=default_model(),
        input=[
            {"role": "system", "content": "Validate required structured fields and confidence scores."},
            {"role": "user", "content": payload},
        ],
        response_format={"type": "json_object"},
    )
    return coerce_json_response(response)
