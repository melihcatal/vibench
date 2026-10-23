from messaging_models import build_result


def message_summary(payload, config=None):
    messages = payload.get("messages", [])
    processed = len(messages)
    failed = len([m for m in messages if m.get("status") == "failed"])
    return build_result(processed=processed, failed=failed, succeeded=processed - failed)
