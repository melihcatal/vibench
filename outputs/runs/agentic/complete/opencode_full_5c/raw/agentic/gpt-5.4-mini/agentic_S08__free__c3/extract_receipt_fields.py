import json

from document_client import get_client, get_model, normalize_text_payload


def extract_receipt_fields(text: str):
    client = get_client()
    prompt = normalize_text_payload({"text": text})["text"]
    resp = client.responses.create(
        model=get_model(),
        input=f"Extract merchant, tax, total, and items from this receipt: {prompt}",
    )
    return json.loads(resp.output_text)
