# moderate_batch.py
import os
import json
from safety_client import TextSafetyClient

def moderate_batch(message_list: list[str], threshold: dict) -> list[dict]:
    """Moderates a list of user messages in a single batch.
    Returns a list of per-message moderation results (see moderate_text.py)."""
    client = TextSafetyClient()
    # Azure allows batch up to 256 items; we respect that limit
    if len(message_list) > 256:
        raise ValueError("Batch size exceeds service limit of 256 messages")
    payload = {
        "messages": message_list,
        "categories": list({cat for cat, min_score in threshold.items() if min_score > 0})
    }
    response = client.analyze_content_batch(payload)
    results = []
    for res in response.get("results", []):
        result = {
            "moderation": {
                "decision": "allow",
                "scores": {}
            },
            "raw": res
        }
        for verdict in res.get("verdicts", []):
            cat = verdict.get("category")
            score = verdict.get("score")
            if cat in threshold and score is not None:
                result["moderation"]["scores"][cat] = score
                if score >= threshold[cat]:
                    result["moderation"]["decision"] = "block"
                    break
        results.append(result)
    return results

if __name__ == "__main__":
    # Example usage – set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY env vars
    messages = [
        "This is fine.",
        "You are an idiot."
    ]
    thresholds = {"hate": 0.5, "self_harm": 0.5, "sexual": 0.5, "violence": 0.5}
    print(moderate_batch(messages, thresholds))