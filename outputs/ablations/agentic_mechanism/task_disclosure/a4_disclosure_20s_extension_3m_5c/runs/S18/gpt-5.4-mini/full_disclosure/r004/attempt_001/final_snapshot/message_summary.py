from dataclasses import asdict
from typing import Any, Dict, Iterable, List, Mapping, Optional

from google.cloud import pubsub_v1

from messaging_models import MessageSummary


def _normalize_record(record: Mapping[str, Any]) -> Dict[str, Any]:
    normalized = dict(record)
    normalized["status"] = str(normalized.get("status", "")).strip().lower()
    normalized["message_id"] = str(normalized.get("message_id", "")).strip()
    return normalized


def summarize_message_processing(records: Iterable[Mapping[str, Any]], details: Optional[Dict[str, Any]] = None) -> MessageSummary:
    total = 0
    succeeded = 0
    failed = 0
    status_counts: Dict[str, int] = {}
    message_ids: List[str] = []

    for record in records:
        normalized = _normalize_record(record)
        total += 1
        status = normalized.get("status", "")
        status_counts[status] = status_counts.get(status, 0) + 1
        message_id = normalized.get("message_id", "")
        if message_id:
            message_ids.append(message_id)
        if status in {"ok", "success", "succeeded", "processed"}:
            succeeded += 1
        else:
            failed += 1

    summary_details = dict(details or {})
    summary_details["status_counts"] = status_counts
    summary_details["message_ids"] = message_ids
    summary_details["provider"] = "google-cloud-pubsub"
    return MessageSummary(total=total, succeeded=succeeded, failed=failed, details=summary_details).normalized()


def summarize_batch_response(response: Any, details: Optional[Dict[str, Any]] = None) -> MessageSummary:
    records: List[Mapping[str, Any]] = []
    if hasattr(response, "results"):
        for item in getattr(response, "results"):
            records.append({"message_id": getattr(item, "message_id", ""), "status": getattr(item, "status", "success")})
    elif isinstance(response, Mapping):
        results = response.get("results", [])
        for item in results:
            if isinstance(item, Mapping):
                records.append(item)
            else:
                records.append({"message_id": getattr(item, "message_id", ""), "status": getattr(item, "status", "success")})
    return summarize_message_processing(records, details=details)


def summary_to_dict(summary: MessageSummary) -> Dict[str, Any]:
    return asdict(summary)
