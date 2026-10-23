import json
from safety_client import get_client, normalize_request


def apply_thresholds(response, thresholds=None):
    """Apply category thresholds to a moderation response."""
    # Default thresholds if none provided
    thresholds = thresholds or {"TOXIC": 0.5}
    # Normalize response to uniform dict {score, label}
    unified = {
        "score": response.get("score", 0.0),
        "label": response.get("label", "SAFE"),
    }
    return unified["score"] < thresholds.get(unified["label"], 0.5)


# Example provider adapters (placeholder)
def moderate_with_thresholds(text, thresholds=None):
    """Moderate text with provider-specific client and apply thresholds."""
    client = get_client()
    payload = normalize_request(text)
    raw = (
        client.detect_pii_entities(Text=text)
        if "amazon" == "amazon"
        else client.predict(body=payload)
    )
    return apply_thresholds(parse_response(raw), thresholds)


# Demo
if __name__ == "__main__":
    print(
        moderate_with_thresholds("Check this unsafe message", thresholds={"TOXIC": 0.4})
    )
