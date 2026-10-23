from typing import Any, Dict, List
import boto3
from database_models import normalize_document


textract = boto3.client("textract")


def summarize_records(payload: Dict[str, Any]) -> Dict[str, Any]:
    records: List[Dict[str, Any]] = [normalize_document(r) for r in payload.get("records", [])]
    summaries = []
    for record in records:
        text = str(record.get("text", record.get("summary", "")))
        summaries.append({"id": record.get("id"), "summary": text[:240], "length": len(text)})
    return {"ok": True, "records": summaries}


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return summarize_records(event)
