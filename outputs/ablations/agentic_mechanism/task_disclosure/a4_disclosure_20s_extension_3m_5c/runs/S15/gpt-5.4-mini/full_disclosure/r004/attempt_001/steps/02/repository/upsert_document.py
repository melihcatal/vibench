import json
import os
from typing import Any, Dict, Optional

import requests


AZURE_COSMOS_ENDPOINT_ENV = "AZURE_COSMOS_ENDPOINT"
AZURE_COSMOS_KEY_ENV = "AZURE_COSMOS_KEY"
AZURE_COSMOS_DATABASE_ENV = "AZURE_COSMOS_DATABASE"
AZURE_COSMOS_CONTAINER_ENV = "AZURE_COSMOS_CONTAINER"
AZURE_COSMOS_API_VERSION = "2018-12-31"


def _load_document(document: Any) -> Dict[str, Any]:
    if isinstance(document, dict):
        return dict(document)
    if isinstance(document, str):
        return json.loads(document)
    raise TypeError("document must be a mapping or JSON string")


def _document_id(document: Dict[str, Any], document_id: Optional[str]) -> str:
    if document_id is not None:
        return str(document_id)
    for key in ("id", "_id", "documentId", "document_id"):
        if key in document and document[key] is not None:
            return str(document[key])
    raise ValueError("a primary identifier is required")


def upsert_document(document: Any, document_id: Optional[str] = None) -> Dict[str, Any]:
    endpoint = os.environ[AZURE_COSMOS_ENDPOINT_ENV].rstrip("/")
    key = os.environ[AZURE_COSMOS_KEY_ENV]
    database = os.environ[AZURE_COSMOS_DATABASE_ENV]
    container = os.environ[AZURE_COSMOS_CONTAINER_ENV]

    payload = _load_document(document)
    doc_id = _document_id(payload, document_id)
    payload["id"] = doc_id

    resource_link = f"dbs/{database}/colls/{container}/docs/{doc_id}"
    url = f"{endpoint}/{resource_link}"
    headers = {
        "Authorization": key,
        "x-ms-date": requests.utils.formatdate(usegmt=True),
        "x-ms-version": AZURE_COSMOS_API_VERSION,
        "Content-Type": "application/json",
    }

    response = requests.put(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    if response.content:
        return response.json()
    return payload


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: upsert_document.py <document-json-or-path>")
    arg = sys.argv[1]
    if os.path.exists(arg):
        with open(arg, "r", encoding="utf-8") as handle:
            document = handle.read()
    else:
        document = arg
    result = upsert_document(document)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
