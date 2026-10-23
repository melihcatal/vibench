import os
from typing import List, Dict, Any
from safety_client import SafetyClient


def moderate_batch(messages: List[str]) -> List[Dict[str, Any]]:
    """
    Moderate a batch of user messages and return per-message decisions.

    Args:
        messages: List of text messages to moderate

    Returns:
        List of moderation results for each message
    """
    client = SafetyClient.get_client()
    results = []

    # Use Google Perspective API for batch moderation
    from googleapiclient import discovery
    import google.auth

    # Get credentials
    credentials, project = google.auth.default()

    # Create the Perspective API client
    perspective_client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        credentials=credentials,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    for i, message in enumerate(messages):
        try:
            analyze_request = {
                "comment": {"text": message},
                "requestedAttributes": {
                    "TOXICITY": {},
                    "SEVERE_TOXICITY": {},
                    "IDENTITY_ATTACK": {},
                    "INSULT": {},
                    "PROFANITY": {},
                    "THREAT": {},
                },
                "languages": ["en"],
                "doNotStore": True,
            }

            response = (
                perspective_client.comments().analyze(body=analyze_request).execute()
            )

            # Extract scores
            scores = {}
            decisions = {}
            for attr_name, attr_data in response.get("attributeScores", {}).items():
                score = attr_data.get("summaryScore", {}).get("value", 0)
                scores[attr_name] = score
                decisions[attr_name] = score > 0.7  # Threshold for flagging

            # Overall decision
            flagged = any(decisions.values())

            results.append(
                {
                    "message_index": i,
                    "text": message,
                    "flagged": flagged,
                    "scores": scores,
                    "decisions": decisions,
                    "provider": "google_perspective",
                    "model": "perspective-api-v1alpha1",
                }
            )

        except Exception as e:
            results.append(
                {
                    "message_index": i,
                    "text": message,
                    "flagged": False,
                    "error": str(e),
                    "provider": "google_perspective",
                    "model": "perspective-api-v1alpha1",
                }
            )

    return results
