import boto3


def metric_annotation_safety(payload, config=None):
    client = boto3.client("comprehend", region_name=(config or {}).get("region"))
    text = payload.get("text", "")
    response = client.detect_pii_entities(Text=text, LanguageCode=payload.get("language", "en"))
    unsafe = any(entity["Type"] in {"PASSWORD", "BANK_ACCOUNT_NUMBER", "CREDIT_DEBIT_NUMBER"} for entity in response.get("Entities", []))
    return {"safe": not unsafe, "entities": response.get("Entities", [])}
