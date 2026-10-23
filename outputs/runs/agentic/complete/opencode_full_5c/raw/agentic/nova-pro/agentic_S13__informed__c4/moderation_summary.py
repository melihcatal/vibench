from .safety_client import create_client, moderate_text


def moderation_summary(messages):
    client = create_client()
    results = moderate_batch(client, messages)
    summary = {"safe": 0, "unsafe": 0}
    for result in results:
        if result["categories"]["toxicity"]["score"] > 0.5:
            summary["unsafe"] += 1
        else:
            summary["safe"] += 1
    return summary
