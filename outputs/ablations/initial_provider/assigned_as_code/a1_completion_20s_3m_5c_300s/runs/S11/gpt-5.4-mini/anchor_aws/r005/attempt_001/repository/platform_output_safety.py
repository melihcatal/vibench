import boto3

from model_client import get_region


def platform_output_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=get_region(config))
    response = client.detect_pii_entities(Text=payload["text"], LanguageCode=config.get("language_code", "en"))
    unsafe = any(entity.get("Type") in {"SSN", "BANK_ACCOUNT_NUMBER", "CREDIT_DEBIT_NUMBER", "PASSWORD"} for entity in response.get("Entities", []))
    return {"unsafe": unsafe, "entities": response.get("Entities", []), "response": response}
