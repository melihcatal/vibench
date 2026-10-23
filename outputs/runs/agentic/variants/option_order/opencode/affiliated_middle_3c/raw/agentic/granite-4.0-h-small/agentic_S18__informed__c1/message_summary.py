# message_summary.py
# [LATER-STEP]
# Summarize message processing results after batch consumption

import json
from typing import List, Dict


def summarize(raw_messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Produce a summary dict from a list of processed message dicts.

    Summary includes totals, timestamps, and a snapshot of payload stats.
    """
    summary = {
        "processedCount": len(raw_messages),
        "uniqueEventIds": set(),
        "earliestTimestamp": None,
        "latestTimestamp": None,
        "payloadStats": {"minSize": None, "maxSize": None, "avgSize": None},
    }

    for msg in raw_messages:
        summary["uniqueEventIds"].add(msg.get("id"))
        ts = msg.get("timestamp")
        if ts is not None:
            if (
                summary["earliestTimestamp"] is None
                or ts < summary["earliestTimestamp"]
            ):
                summary["earliestTimestamp"] = ts
            if summary["latestTimestamp"] is None or ts > summary["latestTimestamp"]:
                summary["latestTimestamp"] = ts
        payload = msg.get("payload")
        if isinstance(payload, dict):
            size = len(json.dumps(payload))
            if (
                summary["payloadStats"]["minSize"] is None
                or size < summary["payloadStats"]["minSize"]
            ):
                summary["payloadStats"]["minSize"] = size
            if (
                summary["payloadStats"]["maxSize"] is None
                or size > summary["payloadStats"]["maxSize"]
            ):
                summary["payloadStats"]["maxSize"] = size
            if summary["payloadStats"]["avgSize"] is None:
                summary["payloadStats"]["avgSize"] = size
            else:
                # running average
                summary["payloadStats"]["avgSize"] = (
                    summary["payloadStats"]["avgSize"] * (summary["processedCount"] - 1)
                    + size
                ) / summary["processedCount"]
        else:
            summary["payloadStats"]["minSize"] = 0
            summary["payloadStats"]["maxSize"] = 0
            summary["payloadStats"]["avgSize"] = 0

    summary["uniqueEventIds"] = list(summary["uniqueEventIds"])
    return summary


if __name__ == "__main__":
    # Simple CLI demo: load a JSON lines file where each line is a message
    import sys

    if len(sys.argv) != 2:
        print("Usage: python message_summary.py <messages.jsonl>")
        sys.exit(1)
    messages: List[Dict[str, Any]] = []
    with open(sys.argv[1], "r") as f:
        for line in f:
            messages.append(json.loads(line.strip()))
    print(json.dumps(summarize(messages), indent=2))
