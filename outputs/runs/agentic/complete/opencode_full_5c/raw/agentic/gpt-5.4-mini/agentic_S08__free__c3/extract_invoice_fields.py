import json

from document_client import get_client, get_model, normalize_text_payload


def extract_invoice_fields(text: str):
    client = get_client()
    prompt = normalize_text_payload({"text": text})["text"]
    resp = client.responses.create(
        model=get_model(),
        input=f"Extract vendor, date, total, and line-item fields from this invoice: {prompt}",
    )
    return json.loads(resp.output_text)
