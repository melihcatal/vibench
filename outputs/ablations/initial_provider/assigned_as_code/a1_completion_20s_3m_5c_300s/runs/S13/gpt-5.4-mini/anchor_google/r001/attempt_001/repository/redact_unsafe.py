from safety_client import post_perspective


def redact_unsafe(payload, config=None):
    text = payload["text"]
    data = post_perspective({"comment": {"text": text}, "languages": ["en"], "requestedAttributes": {"TOXICITY": {}}, "doNotStore": True}, config=config)
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    if score < (config or {}).get("threshold", 0.5):
        return {"text": text, "redacted": False, "toxicity": score}
    return {"text": "[REDACTED]", "redacted": True, "toxicity": score}
