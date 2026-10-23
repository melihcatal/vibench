from collections import Counter

from google.cloud import aiplatform


def summarize(entries: list) -> dict:
    aiplatform.init()
    severities = Counter(entry.get("severity", "UNKNOWN") for entry in entries)
    messages = [entry.get("message", "") for entry in entries[:10]]
    return {
        "total": len(entries),
        "severity_counts": dict(severities),
        "sample_messages": messages,
    }


if __name__ == "__main__":
    summarize([])
