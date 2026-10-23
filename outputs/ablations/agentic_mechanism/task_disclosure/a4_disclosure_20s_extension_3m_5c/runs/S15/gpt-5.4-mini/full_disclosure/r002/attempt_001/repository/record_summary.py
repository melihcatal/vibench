import os
from typing import Any, Dict, Iterable, List, Mapping, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from database_models import normalize_document


class RecordSummaryError(Exception):
    pass


def _table_name() -> str:
    table_name = os.getenv("DYNAMODB_TABLE_NAME") or os.getenv("AWS_DYNAMODB_TABLE_NAME")
    if not table_name:
        raise RecordSummaryError("Missing DYNAMODB_TABLE_NAME")
    return table_name


def _primary_key_name() -> str:
    return os.getenv("DYNAMODB_PRIMARY_KEY", "id")


def _dynamodb_resource():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return boto3.resource("dynamodb", region_name=region)


def _summarize_text(value: Any, max_length: int = 180) -> str:
    if value is None:
        return ""
    text = str(value).strip().replace("
", " ").replace("
", " ")
    if len(text) <= max_length:
        return text
    return text[: max_length - 1].rstrip() + "…"


def _pick_fields(document: Mapping[str, Any], preferred_fields: Iterable[str]) -> Dict[str, Any]:
    summary: Dict[str, Any] = {}
    for field in preferred_fields:
        if field in document and document[field] not in (None, "", [], {}):
            summary[field] = document[field]
    return summary


def summarize_record(document: Mapping[str, Any], fields: Optional[List[str]] = None, max_length: int = 180) -> Dict[str, Any]:
    normalized = normalize_document(document)
    preferred_fields = fields or ["title", "name", "subject", "summary", "description", "status"]
    picked = _pick_fields(normalized, preferred_fields)
    text_fragments = []
    for key, value in picked.items():
        text_fragments.append(f"{key}: {_summarize_text(value, max_length=max_length)}")
    if not text_fragments:
        for key, value in list(normalized.items())[:5]:
            if isinstance(value, (dict, list)):
                continue
            text_fragments.append(f"{key}: {_summarize_text(value, max_length=max_length)}")
    return {"summary": " | ".join(text_fragments), "fields": picked, "document": normalized}


def summarize_retrieved_document(identifier: Any, primary_key: Optional[str] = None, fields: Optional[List[str]] = None, max_length: int = 180) -> Dict[str, Any]:
    key_name = primary_key or _primary_key_name()
    if identifier is None:
        raise RecordSummaryError(f"Missing primary identifier '{key_name}'")

    table = _dynamodb_resource().Table(_table_name())
    try:
        response = table.get_item(Key={key_name: identifier})
    except (BotoCoreError, ClientError) as exc:
        raise RecordSummaryError(str(exc)) from exc

    item = response.get("Item")
    if item is None:
        return {"ok": False, "found": False, "table": _table_name(), "primary_key": key_name, "primary_id": identifier, "summary": "", "document": None}

    summary = summarize_record(item, fields=fields, max_length=max_length)
    return {"ok": True, "found": True, "table": _table_name(), "primary_key": key_name, "primary_id": identifier, "summary": summary["summary"], "document": summary["document"], "fields": summary["fields"], "response": response}
