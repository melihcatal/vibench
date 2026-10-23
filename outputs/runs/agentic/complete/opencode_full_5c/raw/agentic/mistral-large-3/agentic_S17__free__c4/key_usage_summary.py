from datetime import datetime
from typing import List, Dict
import json


def summarize_key_usage(events: List[Dict]) -> dict:
    summary = {
        "total_operations": len(events),
        "operations_by_type": {},
        "operations_by_key": {},
        "timestamp_range": {
            "start": None,
            "end": None,
        },
        "providers": set(),
    }

    for event in events:
        op_type = event.get("operation", "unknown")
        key_id = event.get("key_id", "unknown")
        provider = event.get("provider", "google_kms")
        timestamp = event.get("timestamp", None)

        summary["providers"].add(provider)

        if timestamp:
            if (
                summary["timestamp_range"]["start"] is None
                or timestamp < summary["timestamp_range"]["start"]
            ):
                summary["timestamp_range"]["start"] = timestamp
            if (
                summary["timestamp_range"]["end"] is None
                or timestamp > summary["timestamp_range"]["end"]
            ):
                summary["timestamp_range"]["end"] = timestamp

        summary["operations_by_type"][op_type] = (
            summary["operations_by_type"].get(op_type, 0) + 1
        )
        summary["operations_by_key"][key_id] = (
            summary["operations_by_key"].get(key_id, 0) + 1
        )

    summary["providers"] = list(summary["providers"])
    return summary


def log_crypto_event(
    operation: str,
    key_id: str,
    algorithm: str,
    provider: str = "google_kms",
    metadata: Dict = None,
) -> dict:
    event = {
        "operation": operation,
        "key_id": key_id,
        "algorithm": algorithm,
        "provider": provider,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata": metadata or {},
    }
    return event
