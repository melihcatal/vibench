from safety_client import perspective_request
from safety_models import normalize_messages


def moderate_batch(payload, config=None):
    results = []
    for message in normalize_messages(payload):
        data = perspective_request(message["text"], {"TOXICITY": {}}, config=config)
        score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        results.append({"text": message["text"], "toxicity": score, "allow": score < (config or {}).get("threshold", 0.5)})
    return {"results": results}
