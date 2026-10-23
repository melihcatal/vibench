import json
import os
import sys
from collections import Counter
from datetime import datetime
from typing import Any, Iterable

import boto3


def _load_records(source: str) -> list[dict[str, Any]]:
    data = json.loads(source)
    if isinstance(data, dict):
        for key in ("items", "records", "documents", "results"):
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [data]
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    raise ValueError("input must be a JSON object or array")


def _count_words(text: str) -> int:
    return len([part for part in text.split() if part])


def _record_text(record: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ("title", "summary", "content", "body", "text", "description"):
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            parts.append(value.strip())
    if not parts:
        for value in record.values():
            if isinstance(value, str) and value.strip():
                parts.append(value.strip())
    return " ".join(parts)


def summarize_records(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    records = list(records)
    sources = Counter()
    total_words = 0
    dated = 0
    for record in records:
        source = record.get("source") or record.get("provider") or record.get("collection") or "unknown"
        sources[str(source)] += 1
        total_words += _count_words(_record_text(record))
        if any(isinstance(record.get(field), str) for field in ("created_at", "updated_at", "timestamp")):
            dated += 1
    return {
        "record_count": len(records),
        "source_counts": dict(sources),
        "total_words": total_words,
        "average_words": round(total_words / len(records), 2) if records else 0,
        "records_with_dates": dated,
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }


def main() -> None:
    table_name = os.environ.get("DYNAMODB_TABLE_NAME")
    region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
    if not table_name:
        raise SystemExit("DYNAMODB_TABLE_NAME is required")
    payload = sys.stdin.read()
    if not payload.strip():
        dynamodb = boto3.resource("dynamodb", region_name=region)
        table = dynamodb.Table(table_name)
        response = table.scan()
        records = list(response.get("Items", []))
        while "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            records.extend(response.get("Items", []))
    else:
        records = _load_records(payload)
    print(json.dumps(summarize_records(records), default=str))


if __name__ == "__main__":
    main()
