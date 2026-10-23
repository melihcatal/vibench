from google.cloud import firestore
from messaging_client import get_pubsub_config


def summarize_message_processing(results):
    total = len(results)
    successes = sum(1 for item in results if item.get("status") == "success")
    failures = total - successes
    return {"total": total, "successes": successes, "failures": failures}
