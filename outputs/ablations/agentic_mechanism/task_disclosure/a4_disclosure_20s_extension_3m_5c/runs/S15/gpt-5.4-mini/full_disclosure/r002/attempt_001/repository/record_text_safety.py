import os
from typing import Any, Dict, List, Mapping, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from database_models import normalize_document


class RecordTextSafetyError(Exception):
    pass


def _table_name() -> str:
    table_name = os.getenv("DYNAMODB_TABLE_NAME") or os.getenv("AWS_DYNAMODB_TABLE_NAME")
    if not table_name:
        raise RecordTextSafetyError("Missing DYNAMODB_TABLE_NAME")
    return table_name


def _primary_key_name() -> str:
    return os.getenv("DYNAMODB_PRIMARY_KEY", "id")


def _dynamodb_resource():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return boto3.resource("dynamodb", region_name=region)


def _safe_fields() -> List[str]:
    raw = os.getenv("TEXT_SAFETY_FIELDS")
    if raw:
        fields = [part.strip() for part in raw.split(",") if part.strip()]
        if fields:
            return fields
    return ["title", "name", "subject", "summary", "description", "body", "content", "message", "comment"]


def _openai_client() -> Any:
    from openai import OpenAI

    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _extract_text(document: Mapping[str, Any], fields: Optional[List[str]] = None) -> str:
    normalized = normalize_document(document)
    target_fields = fields or _safe_fields()
    fragments: List[str] = []
    for field in target_fields:
        value = normalized.get(field)
        if value is None or value == "":
            continue
        fragments.append(f"{field}: {value}")
    if fragments:
        return "\n".join(fragments)
    for key, value in normalized.items():
        if isinstance(value, (dict, list)):
            continue
        fragments.append(f"{key}: {value}")
    return "\n".join(fragments)


def assess_text_safety(text: str, model: str = "omni-moderation-latest") -> Dict[str, Any]:
    if not text.strip():
        return {"safe": True, "flagged": False, "categories": {}, "category_scores": {}, "model": model, "raw": {}}
    client = _openai_client()
    response = client.moderations.create(model=model, input=text)
    result = response.results[0]
    return {
        "safe": not bool(result.flagged),
        "flagged": bool(result.flagged),
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
        "model": model,
        "raw": response.model_dump() if hasattr(response, "model_dump") else {},
    }


def check_record_text_safety(document: Mapping[str, Any], fields: Optional[List[str]] = None, model: str = "omni-moderation-latest") -> Dict[str, Any]:
    normalized = normalize_document(document)
    text = _extract_text(normalized, fields=fields)
    assessment = assess_text_safety(text, model=model)
    return {"document": normalized, "text": text, **assessment}


def check_retrieved_document_text_safety(identifier: Any, primary_key: Optional[str] = None, fields: Optional[List[str]] = None, model: str = "omni-moderation-latest") -> Dict[str, Any]:
    key_name = primary_key or _primary_key_name()
    if identifier is None:
        raise RecordTextSafetyError(f"Missing primary identifier '{key_name}'")

    table = _dynamodb_resource().Table(_table_name())
    try:
        response = table.get_item(Key={key_name: identifier})
    except (BotoCoreError, ClientError) as exc:
        raise RecordTextSafetyError(str(exc)) from exc

    item = response.get("Item")
    if item is None:
        return {"ok": False, "found": False, "table": _table_name(), "primary_key": key_name, "primary_id": identifier, "safe": True, "flagged": False, "categories": {}, "category_scores": {}, "model": model, "document": None, "text": ""}

    assessment = check_record_text_safety(item, fields=fields, model=model)
    return {"ok": True, "found": True, "table": _table_name(), "primary_key": key_name, "primary_id": identifier, **assessment, "response": response}
