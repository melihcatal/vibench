import os
import json

# Tisane Text Moderation service integration (same-scenario)
TISANE_API_KEY = os.getenv("TISANE_API_KEY")
TISANE_ENDPOINT = "https://api.tisane.ai/parse"


def build_moderation_request(messages: list[str], attribute: str = "offensive"):
    """Creates a request payload for Tisane Text Moderation.

    Args:
        messages (list[str]): User messages to moderate.
        attribute (str): Attribute to check, default 'offensive'.

    Returns:
        dict: JSON-ready request body.
    """
    return {
        "input": "\n".join(messages),
        "settings": {"offensiveness": {"enabled": True, "attribute": attribute}},
    }


def parse_moderation_response(response_json) -> list[dict]:
    """Parses Tisane response into a consistent moderation result list.

    Args:
        response_json (dict): Raw response from Tisane API.

    Returns:
        list[dict]: Each dict contains { 'message': original, 'severity': <LOW/MEDIUM/HIGH>, 'passes': bool }
    """
    results = []
    for entry in response_json.get("results", []):
        # Tisane returns scores 0-1 for offensiveness
        score = entry.get("offensiveness", 0)
        if score is None:
            score = 0
        severity = "LOW"
        if score > 0.7:
            severity = "HIGH"
        elif score > 0.4:
            severity = "MEDIUM"
        # Assume message index matches input order
        orig_msg = entry.get("text", "")
        results.append(
            {"message": orig_msg, "severity": severity, "passes": severity == "LOW"}
        )
    return results
