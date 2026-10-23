from document_client import get_openai_client, default_model
from document_models import coerce_json_response


def invoice_summary(extracted_invoice_fields: dict):
    client = get_openai_client()
    response = client.responses.create(
        model=default_model(),
        input=[
            {"role": "system", "content": "Summarize extracted invoice fields succinctly."},
            {"role": "user", "content": str(extracted_invoice_fields)},
        ],
        response_format={"type": "json_object"},
    )
    return coerce_json_response(response)
