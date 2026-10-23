from safety_client import post_perspective
from safety_models import decision_from_score


def safety_threshold(payload, config=None):
    thresholds = (config or {}).get("thresholds") or {"TOXICITY": 0.5}
    data = post_perspective({"comment": {"text": payload["text"]}, "languages": ["en"], "requestedAttributes": {"TOXICITY": {}}, "doNotStore": True}, config=config)
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return {"decision": decision_from_score(score, thresholds["TOXICITY"]), "toxicity": score}
