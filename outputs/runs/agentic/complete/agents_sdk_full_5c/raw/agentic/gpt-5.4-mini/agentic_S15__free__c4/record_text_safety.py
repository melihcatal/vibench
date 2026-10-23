from __future__ import annotations

from typing import Any, Dict, Mapping

import boto3

from database_models import extract_field_text


def record_text_safety(record: Mapping[str, Any]) -> Dict[str, Any]:
    client = boto3.client("comprehend", region_name="us-east-1")
    text = extract_field_text(record, ["title", "body", "content", "notes"])
    response = client.detect_pii_entities(Text=text, LanguageCode="en")
    entities = response.get("Entities", [])
    unsafe = any(entity.get("Type") in {"SSN", "BANK_ACCOUNT_NUMBER", "PASSWORD", "CREDIT_DEBIT_NUMBER"} for entity in entities)
    return {"unsafe": unsafe, "entities": entities}
