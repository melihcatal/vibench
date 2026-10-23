from safety_client import post_perspective
from safety_models import normalize_texts


def moderate_batch(payload, config=None):
    texts = normalize_texts(payload)
    threshold = (config or {}).get("threshold", 0.5)
    results = []
    for text in texts:
        data = post_perspective({"comment": {"text": text}, "languages": ["en"], "requestedAttributes": {"TOXICITY": {}}, "doNotStore": True}, config=config)
        score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        results.append({"text": text, "decision": score < threshold, "toxicity": score})
    return {"results": results}
