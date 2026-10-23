from messaging_models import MessagePayload
from typing import List


def summarize(messages: List[MessagePayload]) -> dict:
    """
    Aggregate statistics about a batch of processed messages.

    Returns a dict with total count, earliest timestamp, latest timestamp,
    and a breakdown per user_id.
    """
    if not messages:
        return {"total": 0, "earliest": None, "latest": None, "per_user": {}}

    total = len(messages)
    timestamps = [msg.timestamp for msg in messages]
    earliest = min(timestamps)
    latest = max(timestamps)

    per_user = {}
    for msg in messages:
        uid = msg.user_id
        per_user[uid] = per_user.get(uid, 0) + 1

    return {
        "total": total,
        "earliest": earliest,
        "latest": latest,
        "per_user": per_user,
    }
