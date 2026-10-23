from collections import Counter

from messaging_models import IntegrationResponse


def summarize_messages(results):
    provider = "google_pubsub"
    counts = Counter()
    message_ids = []
    for result in results:
        counts[result.get("status", "unknown")] += 1
        message_ids.extend(result.get("message_ids", []))
    summary = {"total": len(results), "status_counts": dict(counts), "message_ids": message_ids}
    return IntegrationResponse(provider=provider, resource="message_summary", details=summary)
