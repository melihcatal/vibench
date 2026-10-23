from speech_client import load_config

import boto3


def script_safety(payload, config=None):
    cfg = load_config(config)
    client = boto3.client("comprehend", region_name=cfg["region"])
    text = payload["text"]
    response = client.detect_pii_entities(Text=text, LanguageCode=payload.get("language", "en"))
    unsafe = [item for item in response.get("Entities", []) if item.get("Type") in {"SSN", "PASSPORT_NUMBER", "BANK_ACCOUNT_NUMBER", "CREDIT_DEBIT_NUMBER"}]
    return {"safe": not bool(unsafe), "entities": response.get("Entities", [])}
