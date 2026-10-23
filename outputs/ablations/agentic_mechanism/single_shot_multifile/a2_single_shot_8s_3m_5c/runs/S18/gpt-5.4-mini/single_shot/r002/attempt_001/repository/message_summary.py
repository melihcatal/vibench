from collections import Counter
from messaging_models import success_result


def message_summary(records):
    total = len(records or [])
    statuses = Counter()
    for record in records or []:
        statuses[str(record.get("status", "unknown"))] += 1
    return success_result(provider="google_cloud_pubsub", operation="message_summary", total=total, statuses=dict(statuses))
