from typing import Any, Dict, Iterable, List

from google.cloud import firestore

from messaging_models import normalize_json_payload


def summarize_message_processing(results: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    items = [normalize_json_payload(result) for result in results]
    processed = len(items)
    successes = sum(1 for item in items if isinstance(item, dict) and item.get("status") == "success")
    failures = processed - successes
    return {"processed": processed, "successes": successes, "failures": failures, "items": items}


def store_summary(summary: Dict[str, Any], collection_name: str = "message_summaries") -> str:
    client = firestore.Client()
    doc_ref = client.collection(collection_name).document()
    doc_ref.set(summary)
    return doc_ref.id
