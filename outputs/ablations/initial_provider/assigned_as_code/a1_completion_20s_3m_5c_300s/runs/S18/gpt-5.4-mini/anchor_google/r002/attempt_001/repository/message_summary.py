from messaging_models import message_record


def message_summary(payload, config=None):
    records = [message_record(**item) for item in payload.get("records", [])]
    return {"count": len(records), "message_ids": [record["message_id"] for record in records]}
