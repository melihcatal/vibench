import boto3

from database_models import build_response


def record_text_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload.get("text") or payload.get("document", {}).get("text") or ""
    result = client.detect_pii_entities(Text=text, LanguageCode=config.get("language_code", "en"))
    unsafe = any(entity.get("Type") in {"PASSWORD", "BANK_ACCOUNT_NUMBER", "CREDIT_DEBIT_NUMBER"} for entity in result.get("Entities", []))
    return build_response({"unsafe": unsafe, "entities": result.get("Entities", [])})
