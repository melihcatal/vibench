from typing import List, Dict
from datetime import datetime
import json


def summarize_key_usage(crypto_events: List[Dict[str, str]]) -> dict:
    summary = {
        "total_events": len(crypto_events),
        "events_by_type": {},
        "events_by_key": {},
        "timestamp_range": {"earliest": None, "latest": None},
    }

    for event in crypto_events:
        event_type = event.get("event_type", "unknown")
        key_id = event.get("key_id", "unknown")
        timestamp = event.get("timestamp", None)

        # Update event type count
        if event_type not in summary["events_by_type"]:
            summary["events_by_type"][event_type] = 0
        summary["events_by_type"][event_type] += 1

        # Update key usage count
        if key_id not in summary["events_by_key"]:
            summary["events_by_key"][key_id] = 0
        summary["events_by_key"][key_id] += 1

        # Update timestamp range
        if timestamp:
            try:
                event_time = datetime.fromisoformat(timestamp)
                if (
                    summary["timestamp_range"]["earliest"] is None
                    or event_time < summary["timestamp_range"]["earliest"]
                ):
                    summary["timestamp_range"]["earliest"] = event_time
                if (
                    summary["timestamp_range"]["latest"] is None
                    or event_time > summary["timestamp_range"]["latest"]
                ):
                    summary["timestamp_range"]["latest"] = event_time
            except ValueError:
                pass

    return summary
