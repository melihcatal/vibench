import json
from document_client import get_google_client, load_config


def extract_invoice_fields(document_text: str) -> dict:
    client = get_google_client()
    cfg = load_config()
    prompt = "Extract vendor, date, total, and line-items as JSON from this invoice."
    response = client.models.generate_content(
        model=cfg.google_model,
        contents=[prompt, document_text],
    )
    return json.loads(response.text)
