from safety_client import perspective_request
from safety_models import redact_spans


def redact_unsafe(payload, config=None):
    text = payload["text"] if isinstance(payload, dict) else str(payload)
    data = perspective_request(text, {"TOXICITY": {}, "INSULT": {}}, config=config)
    spans = []
    for attribute in ("TOXICITY", "INSULT"):
        for span in data.get("attributeScores", {}).get(attribute, {}).get("spanScores", []):
            if span.get("score", {}).get("value", 0) >= (config or {}).get("span_threshold", 0.5):
                spans.append({"start": span["beginOffset"], "end": span["endOffset"]})
    return {"text": redact_spans(text, spans), "redacted": bool(spans)}
