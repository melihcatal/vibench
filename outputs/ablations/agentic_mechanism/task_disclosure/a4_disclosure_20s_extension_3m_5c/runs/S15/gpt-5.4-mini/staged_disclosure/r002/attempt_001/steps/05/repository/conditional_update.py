import os
from typing import Any, Dict, Optional

import requests


COUCHDB_BASE_URL = os.getenv("COUCHDB_BASE_URL", "http://127.0.0.1:5984")
COUCHDB_USERNAME = os.getenv("COUCHDB_USERNAME")
COUCHDB_PASSWORD = os.getenv("COUCHDB_PASSWORD")


def _auth() -> Optional[tuple[str, str]]:
    if COUCHDB_USERNAME and COUCHDB_PASSWORD:
        return COUCHDB_USERNAME, COUCHDB_PASSWORD
    return None


def get_document(database: str, doc_id: str) -> Dict[str, Any]:
    response = requests.get(
        f"{COUCHDB_BASE_URL}/{database}/{doc_id}",
        auth=_auth(),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def conditional_update_document(
    database: str,
    doc_id: str,
    updates: Dict[str, Any],
    expected_rev: Optional[str] = None,
) -> Dict[str, Any]:
    document = get_document(database, doc_id)
    current_rev = document.get("_rev")
    if expected_rev is not None and current_rev != expected_rev:
        raise ValueError(f"revision mismatch: expected {expected_rev}, found {current_rev}")

    document.update(updates)
    response = requests.put(
        f"{COUCHDB_BASE_URL}/{database}/{doc_id}",
        auth=_auth(),
        json=document,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    database = os.environ["COUCHDB_DATABASE"]
    doc_id = os.environ["COUCHDB_DOCUMENT_ID"]
    updates = {"status": os.getenv("COUCHDB_NEW_STATUS", "updated")}
    expected_rev = os.getenv("COUCHDB_EXPECTED_REV")
    result = conditional_update_document(database, doc_id, updates, expected_rev)
    print(result)


if __name__ == "__main__":
    main()
