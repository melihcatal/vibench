from typing import Any, Dict

from document_models import normalize_field_name


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {"provider": extracted.get("provider", "aws_textract"), "fields": {}}
    for key, value in extracted.get("response", {}).items() if isinstance(extracted.get("response"), dict) else []:
        normalized["fields"][normalize_field_name(key)] = value
    if "response" not in extracted:
        normalized["fields"] = {normalize_field_name(k): v for k, v in extracted.items() if k not in {"provider"}}
    return normalized
