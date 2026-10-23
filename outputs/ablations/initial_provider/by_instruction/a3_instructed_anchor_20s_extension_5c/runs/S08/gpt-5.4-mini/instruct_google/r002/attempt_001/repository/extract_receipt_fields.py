import json
from document_client import get_google_client, load_config


def extract_receipt_fields(document_text: str) -> dict:
    client = get_google_client()
    cfg = load_config()
    response = client.models.generate_content(
        model=cfg.google_model,
        contents=["Extract merchant, tax, total, and items as JSON from this receipt.", document_text],
    )
    return json.loads(response.text)
