from document_client import get_openai_client, default_model
from document_models import coerce_json_response


def vendor_text_safety(vendor_text: str):
    client = get_openai_client()
    response = client.responses.create(
        model=default_model(),
        input=[
            {"role": "system", "content": "Moderate vendor notes or memo fields for safety."},
            {"role": "user", "content": vendor_text},
        ],
        response_format={"type": "json_object"},
    )
    return coerce_json_response(response)
