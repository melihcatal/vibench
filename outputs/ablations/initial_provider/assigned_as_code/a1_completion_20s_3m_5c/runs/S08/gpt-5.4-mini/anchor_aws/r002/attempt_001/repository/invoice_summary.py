import boto3


def invoice_summary(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    invoice = payload.get("invoice", payload)
    summary = f"Vendor {invoice.get('vendor', '')} total {invoice.get('total', '')} dated {invoice.get('date', '')}".strip()
    if invoice.get("notes"):
        client.detect_sentiment(Text=invoice["notes"], LanguageCode=config.get("language", "en"))
    return {"summary": summary}
