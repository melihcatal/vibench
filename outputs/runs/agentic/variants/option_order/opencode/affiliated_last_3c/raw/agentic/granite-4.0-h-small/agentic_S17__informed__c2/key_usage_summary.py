import json


def summarize_key_usage(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarize key usage statistics from a list of crypto events.

    Args:
        events: List of dictionaries representing each encryption/decryption or signing event.
               Expected keys: 'key_id', 'operation' ('encrypt','decrypt','sign'), 'timestamp'.

    Returns:
        A dict with counts per operation and earliest/latest timestamps.
    """
    summary = {
        "operation_counts": {"encrypt": 0, "decrypt": 0, "sign": 0},
        "first_timestamp": None,
        "last_timestamp": None,
    }
    for ev in events:
        op = ev.get("operation")
        if op in summary["operation_counts"]:
            summary["operation_counts"][op] += 1
        ts = ev.get("timestamp")
        if ts:
            if summary["first_timestamp"] is None or ts < summary["first_timestamp"]:
                summary["first_timestamp"] = ts
            if summary["last_timestamp"] is None or ts > summary["last_timestamp"]:
                summary["last_timestamp"] = ts
    return summary
