import os
from typing import Any, Dict, List, Optional

from google.cloud import firestore


def _get_client() -> firestore.Client:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
    return firestore.Client(project=project_id) if project_id else firestore.Client()


def query_documents(collection: str, field_name: str, field_value: Any, partition_key: Optional[str] = None, partition_value: Optional[Any] = None, limit: int = 100) -> List[Dict[str, Any]]:
    client = _get_client()
    query = client.collection(collection)
    if partition_key is not None and partition_value is not None:
        query = query.where(partition_key, "==", partition_value)
    query = query.where(field_name, "==", field_value).limit(limit)
    results: List[Dict[str, Any]] = []
    for snapshot in query.stream():
        data = snapshot.to_dict() or {}
        data["id"] = snapshot.id
        results.append(data)
    return results


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Query Firestore documents by field or partition key.")
    parser.add_argument("collection")
    parser.add_argument("field_name")
    parser.add_argument("field_value")
    parser.add_argument("--partition-key")
    parser.add_argument("--partition-value")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    docs = query_documents(
        args.collection,
        args.field_name,
        args.field_value,
        args.partition_key,
        args.partition_value,
        args.limit,
    )
    print(json.dumps(docs, ensure_ascii=False, indent=2, default=str))
