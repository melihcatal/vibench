import json
import os
from typing import Any, Dict, Optional

import requests


COGNITO_HOST = os.environ.get("COGNITO_HOST", "")
COGNITO_APP_CLIENT_ID = os.environ.get("COGNITO_APP_CLIENT_ID", "")
COGNITO_APP_CLIENT_SECRET = os.environ.get("COGNITO_APP_CLIENT_SECRET", "")


def _normalize_document(document: Any) -> Dict[str, Any]:
    if isinstance(document, str):
        return json.loads(document)
    if isinstance(document, dict):
        return document
    raise TypeError("document must be a dict or JSON string")


def _get_primary_id(document: Dict[str, Any], primary_key: str) -> Any:
    if primary_key not in document:
        raise KeyError(f"missing primary identifier: {primary_key}")
    value = document[primary_key]
    if value is None or value == "":
        raise ValueError("primary identifier cannot be empty")
    return value


def upsert_document(document: Any, primary_key: str = "id", endpoint: Optional[str] = None) -> Dict[str, Any]:
    payload = _normalize_document(document)
    doc_id = _get_primary_id(payload, primary_key)
    base_url = endpoint or COGNITO_HOST
    if not base_url:
        raise ValueError("missing endpoint or COGNITO_HOST")
    url = f"{base_url.rstrip('/')}/documents/{doc_id}"
    headers = {"Content-Type": "application/json"}
    if COGNITO_APP_CLIENT_ID and COGNITO_APP_CLIENT_SECRET:
        headers["X-Cognito-App-Client-Id"] = COGNITO_APP_CLIENT_ID
        headers["X-Cognito-App-Client-Secret"] = COGNITO_APP_CLIENT_SECRET
    response = requests.put(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    if response.content:
        try:
            return response.json()
        except ValueError:
            return {"status_code": response.status_code, "text": response.text}
    return {"status_code": response.status_code}


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: upsert_document.py '<json>' [primary_key]")
    document = sys.argv[1]
    primary_key = sys.argv[2] if len(sys.argv) > 2 else "id"
    result = upsert_document(document, primary_key=primary_key)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
