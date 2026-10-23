from google.cloud import pubsub_v1


def message_summary(message_results):
    total = len(message_results)
    successes = sum(1 for item in message_results if item.get("message_id"))
    return {"provider": "google-pubsub", "total": total, "successes": successes, "failures": total - successes}
