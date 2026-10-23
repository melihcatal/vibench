import json
import os
import sys
from typing import Any, Dict, Optional

import requests


UPSTASH_REST_URL = os.getenv("UPSTASH_REST_URL")
UPSTASH_REST_TOKEN = os.getenv("UPSTASH_REST_TOKEN")


def _require_env(name: str, value: Optional[str]) -> str:
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def upsert_document(collection: str, document: Dict[str, Any], primary_id: str = "id") -> Dict[str, Any]:
    rest_url = _require_env("UPSTASH_REST_URL", UPSTASH_REST_URL).rstrip("/")
    token = _require_env("UPSTASH_REST_TOKEN", UPSTASH_REST_TOKEN)

    if primary_id not in document:
        raise ValueError(f"Document must contain primary identifier field '{primary_id}'")

    doc_id = str(document[primary_id])
    url = f"{rest_url}/upsert/{collection}/{doc_id}"
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        data=json.dumps(document),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python upsert_document.py <collection> <json_document> [primary_id]", file=sys.stderr)
        return 2

    collection = sys.argv[1]
    try:
        document = json.loads(sys.argv[2])
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON document: {exc}", file=sys.stderr)
        return 2

    primary_id = sys.argv[3] if len(sys.argv) > 3 else "id"
    try:
        result = upsert_document(collection, document, primary_id)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
