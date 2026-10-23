from safety_client import perspective_request
from safety_models import threshold_allows


def safety_threshold(payload, config=None):
    config = config or {}
    thresholds = config.get("thresholds") or {"TOXICITY": 0.5, "INSULT": 0.6, "THREAT": 0.4}
    text = payload["text"] if isinstance(payload, dict) else str(payload)
    data = perspective_request(text, {k: {} for k in thresholds}, config=config)
    scores = {
        category: data["attributeScores"][category]["summaryScore"]["value"]
        for category in thresholds
    }
    return {"allow": threshold_allows(scores, thresholds), "scores": scores}
