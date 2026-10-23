import json

from document_client import get_client, get_model


def validate_document_fields(fields: dict):
    client = get_client()
    resp = client.responses.create(
        model=get_model(),
        input=f"Validate required structured fields and confidence scores for this document: {json.dumps(fields)}",
    )
    return json.loads(resp.output_text)
