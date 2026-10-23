from typing import Any, Dict, Iterable

from google.cloud import pubsub_v1


def summarize_message_processing(results: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    items = list(results)
    total = len(items)
    success = sum(1 for item in items if item.get("status") == "success")
    failed = total - success
    return {"provider": "google-cloud-pubsub", "total": total, "success": success, "failed": failed, "success_rate": (success / total) if total else 0.0}
