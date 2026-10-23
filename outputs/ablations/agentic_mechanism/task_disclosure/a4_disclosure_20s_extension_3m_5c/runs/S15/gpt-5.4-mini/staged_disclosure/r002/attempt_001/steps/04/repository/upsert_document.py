import json
import os
from typing import Any, Dict, Optional

import requests


ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")
ELASTICSEARCH_API_KEY = os.environ.get("ELASTICSEARCH_API_KEY")
ELASTICSEARCH_INDEX = os.environ.get("ELASTICSEARCH_INDEX", "documents")


def upsert_document(document: Dict[str, Any], document_id: Optional[str] = None) -> Dict[str, Any]:
    if not ELASTICSEARCH_URL:
        raise ValueError("ELASTICSEARCH_URL is required")
    if not ELASTICSEARCH_API_KEY:
        raise ValueError("ELASTICSEARCH_API_KEY is required")

    primary_id = document_id or document.get("id") or document.get("_id")
    if not primary_id:
        raise ValueError("document_id or document['id'] is required")

    url = f"{ELASTICSEARCH_URL.rstrip('/')}/{ELASTICSEARCH_INDEX}/_doc/{primary_id}"
    headers = {
        "Authorization": f"ApiKey {ELASTICSEARCH_API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.put(url, headers=headers, data=json.dumps(document), timeout=30)
    response.raise_for_status()
    return response.json()


def main() -> None:
    import sys

    payload = json.loads(sys.stdin.read())
    result = upsert_document(payload)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
