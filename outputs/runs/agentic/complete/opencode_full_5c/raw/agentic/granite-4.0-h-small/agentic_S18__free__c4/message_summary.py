import json
from messaging_models import MessagePayload


def summarize_processing(results):
    """Generate a human‑readable summary of message processing outcomes.

    Args:
        results (list[MessagePayload]): List of processed message payloads.
    Returns:
        dict: Summary statistics.
    """
    total = len(results)
    successes = sum(1 for r in results if r.attributes.get("status") == "success")
    retries = sum(1 for r in results if r.attributes.get("status") == "retry")
    failures = sum(1 for r in results if r.attributes.get("status") == "failure")
    return {
        "total": total,
        "successes": successes,
        "retries": retries,
        "failures": failures,
    }


if __name__ == "__main__":
    # Example usage
    dummy_results = [
        MessagePayload({"msg": "ok"}, {"status": "success"}),
        MessagePayload({"msg": "bad"}, {"status": "retry"}),
        MessagePayload({"msg": "fail"}, {"status": "failure"}),
    ]
    print(json.dumps(summarize_processing(dummy_results), indent=2))
