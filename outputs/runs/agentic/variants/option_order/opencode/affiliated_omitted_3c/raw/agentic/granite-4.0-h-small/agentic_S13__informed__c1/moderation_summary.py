import json
from safety_client import get_client


def summarize_decisions(decisions, provider="amazon"):
    """Summarize moderation decisions into a concise report."""
    # Simple aggregation: count safe/toxic
    safe = sum(1 for d in decisions if d["label"] == "SAFE")
    toxic = len(decisions) - safe
    return {
        "summary": f"{safe} messages were SAFE, {toxic} flagged as unsafe.",
        "details": [
            {"text": d["text"], "score": d["score"], "label": d["label"]}
            for d in decisions
        ],
    }


# Example usage (replace with real moderation output)
def generate_summary():
    client = get_client()
    # Dummy moderation results
    decisions = [
        {"text": "Hello", "score": 0.1, "label": "SAFE"},
        {"text": "Bad content", "score": 0.8, "label": "TOXIC"},
    ]
    report = summarize_decisions(decisions, provider="amazon")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    generate_summary()
