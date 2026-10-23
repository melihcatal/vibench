from collections import Counter

from observability_client import query_entries


def main() -> dict:
    entries = query_entries('resource.type="global" AND severity>=ERROR', limit=100)
    counts = Counter((entry.get("severity") or "UNKNOWN") for entry in entries)
    return {
        "total": len(entries),
        "by_severity": dict(counts),
        "top_messages": [entry.get("payload") for entry in entries[:5]],
    }


if __name__ == "__main__":
    main()
