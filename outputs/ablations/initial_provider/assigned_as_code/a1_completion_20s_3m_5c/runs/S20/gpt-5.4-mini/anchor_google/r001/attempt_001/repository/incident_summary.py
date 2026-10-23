from collections import Counter


def incident_summary(payload, config=None):
    results = payload.get("results") or []
    severities = Counter()
    messages = []
    for item in results:
        severity = item.get("severity", "DEFAULT")
        severities[severity] += 1
        text = item.get("textPayload") or str(item.get("jsonPayload") or "")
        if text:
            messages.append(text)
    return {
        "total": len(results),
        "severities": dict(severities),
        "highlights": messages[:5],
    }
