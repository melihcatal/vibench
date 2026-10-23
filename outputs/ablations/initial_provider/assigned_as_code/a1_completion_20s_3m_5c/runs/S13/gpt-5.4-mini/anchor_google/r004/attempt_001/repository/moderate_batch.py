from safety_client import perspective_analyze, get_score
from safety_models import normalize_messages


def moderate_batch(payload, config=None):
    config = config or {}
    messages = normalize_messages(payload.get("messages"))
    results = []
    for message in messages:
        analysis = perspective_analyze(message["text"], ["TOXICITY"], config=config)
        score = get_score(analysis, "TOXICITY")
        results.append({"id": message["id"], "allow": score < config.get("threshold", 0.5), "toxicity": score})
    return {"results": results}
