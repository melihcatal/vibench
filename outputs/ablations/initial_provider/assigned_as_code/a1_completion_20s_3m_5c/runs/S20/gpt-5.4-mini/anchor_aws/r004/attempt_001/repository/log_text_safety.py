import boto3


def log_text_safety(payload, config=None):
    client = boto3.client("comprehend", region_name=(config or {}).get("region"))
    response = client.detect_pii_entities(Text=payload["text"], LanguageCode=payload.get("language", "en"))
    unsafe = any(item.get("Type") in {"SSN", "BANK_ACCOUNT_NUMBER", "CREDIT_DEBIT_NUMBER", "PASSPORT_NUMBER"} for item in response.get("Entities", []))
    return {"safe": not unsafe, "entities": response.get("Entities", [])}
