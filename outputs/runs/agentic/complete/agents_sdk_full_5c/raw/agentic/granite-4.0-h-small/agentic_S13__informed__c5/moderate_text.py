# moderate_text.py
import os
import json
from safety_client import TextSafetyClient

def moderate_text(user_text: str, threshold: dict) -> dict:
    """Runs a single text through the moderation service and returns a decision.
    Uses Azure AI Content Safety to assess hate, self-harm, sexual, and violence categories.
    """
    # Helper to turn dict thresholds into a flat set of required categories
    required_categories = {cat for cat, min_score in threshold.items() if min_score > 0}
    # Prepare payload for the service
    payload = {
        "content": user_text,
        "categories": list(required_categories)  # ask the service to score only needed categories
    }
    client = TextSafetyClient()
    response = client.analyze_content(payload)
    # Normalize response (Azure returns a list of verdicts with category and score)
    results = {}
    for verdict in response.get("results", []):
        cat = verdict.get("category")
        score = verdict.get("score")
        if cat in required_categories:
            results[cat] = score
    # Determine overall decision
    decision = "allow"
    for cat, score in results.items():
        if score >= threshold.get(cat, 0):
            decision = "block"
            break
    return {
        "decision": decision,
        "scores": results,
        "raw": response
    }

if __name__ == "__main__":
    # Example usage – requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY env vars
    text = "This is a harmless example text."
    thresholds = {"hate": 0.5, "self_harm": 0.5, "sexual": 0.5, "violence": 0.5}
    print(moderate_text(text, thresholds))