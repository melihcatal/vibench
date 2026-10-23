import json
import os
from typing import Any, Dict, Optional

import requests


OPENSEARCH_HOST = os.environ.get("OPENSEARCH_HOST")
OPENSEARCH_USER = os.environ.get("OPENSEARCH_USER")
OPENSEARCH_PASSWORD = os.environ.get("OPENSEARCH_PASSWORD")


def conditional_update(index: str, document_id: str, updated_fields: Dict[str, Any], version: Optional[int] = None) -> Dict[str, Any]:
    if not OPENSEARCH_HOST:
        raise ValueError("OPENSEARCH_HOST is required")
    if not OPENSEARCH_USER or not OPENSEARCH_PASSWORD:
        raise ValueError("OPENSEARCH_USER and OPENSEARCH_PASSWORD are required")

    url = f"{OPENSEARCH_HOST.rstrip('/')}/{index}/_update/{document_id}"
    payload: Dict[str, Any] = {"doc": updated_fields}
    params: Dict[str, Any] = {}
    if version is not None:
        params["if_seq_no"] = version
        params["if_primary_term"] = 1

    response = requests.post(
        url,
        params=params,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        auth=(OPENSEARCH_USER, OPENSEARCH_PASSWORD),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def update_one_document() -> Dict[str, Any]:
    index = os.environ.get("OPENSEARCH_INDEX", "documents")
    document_id = os.environ.get("OPENSEARCH_DOCUMENT_ID", "1")
    version = os.environ.get("OPENSEARCH_SEQ_NO")
    updated_fields = {
        "status": "updated",
        "last_updated_by": "opensearch",
    }
    seq_no = int(version) if version is not None else None
    return conditional_update(index, document_id, updated_fields, seq_no)


if __name__ == "__main__":
    print(json.dumps(update_one_document(), indent=2, sort_keys=True))
