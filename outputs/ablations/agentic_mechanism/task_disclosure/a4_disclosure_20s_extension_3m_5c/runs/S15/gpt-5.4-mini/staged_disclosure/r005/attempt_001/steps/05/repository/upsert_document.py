import json
import os
from typing import Any, Dict, Optional

import requests


OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "localhost")
OPENSEARCH_PORT = os.getenv("OPENSEARCH_PORT", "9200")
OPENSEARCH_INDEX = os.getenv("OPENSEARCH_INDEX", "documents")
OPENSEARCH_USERNAME = os.getenv("OPENSEARCH_USERNAME", "admin")
OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD", "admin")


def upsert_document(document: Dict[str, Any], doc_id: Optional[str] = None) -> Dict[str, Any]:
    identifier = doc_id or document.get("id")
    if not identifier:
        raise ValueError("Document primary identifier is required")

    url = f"https://{OPENSEARCH_HOST}:{OPENSEARCH_PORT}/{OPENSEARCH_INDEX}/_doc/{identifier}"
    response = requests.put(
        url,
        auth=(OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD),
        headers={"Content-Type": "application/json"},
        data=json.dumps(document),
        timeout=30,
        verify=True,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Usage: python upsert_document.py '<json_document>'")

    document = json.loads(sys.argv[1])
    result = upsert_document(document)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
