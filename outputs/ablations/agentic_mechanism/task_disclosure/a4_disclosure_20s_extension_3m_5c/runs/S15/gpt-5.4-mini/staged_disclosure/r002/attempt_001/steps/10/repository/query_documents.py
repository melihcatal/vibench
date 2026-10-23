import json
import os
import sys
from typing import Any, Dict, List, Optional

import requests


ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")
ELASTICSEARCH_API_KEY = os.environ.get("ELASTICSEARCH_API_KEY")
ELASTICSEARCH_INDEX = os.environ.get("ELASTICSEARCH_INDEX", "documents")


def query_documents(field: str, value: Any, partition_key: Optional[str] = None) -> List[Dict[str, Any]]:
    if not ELASTICSEARCH_URL:
        raise ValueError("ELASTICSEARCH_URL is required")
    if not ELASTICSEARCH_API_KEY:
        raise ValueError("ELASTICSEARCH_API_KEY is required")
    if not field:
        raise ValueError("field is required")

    must_clauses = [{"term": {field: value}}]
    if partition_key is not None:
        must_clauses.append({"term": {"partition_key": partition_key}})

    url = f"{ELASTICSEARCH_URL.rstrip('/')}/{ELASTICSEARCH_INDEX}/_search"
    headers = {
        "Authorization": f"ApiKey {ELASTICSEARCH_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": {"bool": {"must": must_clauses}},
        "size": 100,
    }
    response = requests.get(url, headers=headers, data=json.dumps(payload), timeout=30)
    response.raise_for_status()
    result = response.json()
    hits = result.get("hits", {}).get("hits", [])
    return [hit.get("_source", {}) for hit in hits]


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit("usage: python query_documents.py <field> <value> [partition_key]")
    field = sys.argv[1]
    value = sys.argv[2]
    partition_key = sys.argv[3] if len(sys.argv) > 3 else None
    print(json.dumps(query_documents(field, value, partition_key), sort_keys=True))


if __name__ == "__main__":
    main()
