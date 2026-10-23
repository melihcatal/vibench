# [LATER-STEP] key_usage_summary.py - Summarize key usage and crypto events

import json
from datetime import datetime
from pathlib import Path

# Example log file layout (one JSON entry per line)
LOG_PATH = Path("crypto_events.log")

EVENT_FIELDS = {
    "timestamp": str,
    "service": str,
    "operation": ["ENCRYPT", "DECRYPT", "SIGN", "VERIFY", "WRAP", "UNWRAP"],
    "key_id": str,
    "user": Optional[str],
    "metadata": dict,
}


def load_events() -> List[dict]:
    """Reads the raw log file and returns a list of event dictionaries.
    Lines that cannot be parsed are ignored.
    """
    events = []
    if not LOG_PATH.exists():
        return events
    with LOG_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                events.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    return events


def summarize_usage() -> Dict[str, Any]:
    """Aggregates counts and recent events per service and operation.

    Returns a dictionary structured as:
    {
        \"service_name\": {
            \"operations\": {
                \"ENCRYPT\": {\"count\": int, \"recent\": [event, ...]},
                \"DECRYPT\": {...},
                ...
            },
            \"total_events\": int
        },
        ...
    }
    """
    usage = {}
    events = load_events()
    for ev in events:
        service = ev.get("service", "unknown")
        op = ev.get("operation")
        usage.setdefault(service, {"operations": {}, "total_events": 0})
        usage[service]["total_events"] += 1
        usage[service]["operations"].setdefault(op, {"count": 0, "recent": []})[
            "count"
        ] += 1
        # Keep only the 5 most recent events per operation
        usage[service]["operations"][op]["recent"].append(ev)
        usage[service]["operations"][op]["recent"] = usage[service]["operations"][op][
            "recent"
        ][-5:]
    return usage


def format_summary() -> str:
    """Produces a human‑readable summary string for stakeholders."""
    usage = summarize_usage()
    lines = []
    header = "=== Key Crypto Usage Summary ==="
    footer = "=== End of Summary ==="
    lines.append(header)
    lines.append(f"Generated at: {datetime.utcnow().isoformat()} UTC")
    lines.append("")
    for service, data in usage.items():
        lines.append(f"\nService: {service}")
        ops = data["operations"]
        total = data["total_events"]
        lines.append(f"  Total events: {total}")
        for op, details in ops.items():
            count = details["count"]
            recent = details["recent"]
            lines.append(f"    {op}: {count} occurrences")
            if recent:
                lines.append("      Recent events:")
                for i, e in enumerate(recent, start=1):
                    lines.append(f"        {i}. {json.dumps(e, indent=2)}")
    lines.append(footer)
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_summary())
