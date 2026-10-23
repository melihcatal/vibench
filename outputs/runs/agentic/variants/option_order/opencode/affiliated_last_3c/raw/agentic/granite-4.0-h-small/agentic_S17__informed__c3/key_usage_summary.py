import os
import json
from typing import List, Dict


def summarize_key_usage(events: List[Dict[str, str]]) -> str:
    """Summarize usage patterns from raw event logs.
    Expected event keys: 'timestamp', 'action' (e.g., encrypt, decrypt, sign, verify), 'key_id', 'user'.
    Returns a concise markdown block.
    """
    usage = {}
    for ev in events:
        key = ev.get("key_id")
        action = ev.get("action")
        usage.setdefault(key, {"count": 0, "actions": set()})
        usage[key]["count"] += 1
        usage[key]["actions"].add(action)
    lines = ["**Key Usage Summary**"]
    for key_id, data in usage.items():
        actions = ", ".join(sorted(data["actions"]))
        lines.append(f"- **{key_id}**: {data['count']} operations ({actions})")
    return "\\n".join(lines)


if __name__ == "__main__":
    # Example usage with sample JSON array from stdin
    raw = sys.stdin.read()
    try:
        events = json.loads(raw)
        summary = summarize_key_usage(events)
        print("## Key Usage Summary\\n")
        print(summary)
    except json.JSONDecodeError as e:
        print("Invalid JSON input", file=sys.stderr)
