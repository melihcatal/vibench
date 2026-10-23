import os

import requests

from safety_models import normalize_text_payload, redact_spans


def redact_unsafe(payload, config=None):
    config = config or {}
    data = normalize_text_payload(payload)
    api_key = config.get("api_key") or os.environ["PERSPECTIVE_API_KEY"]
    response = requests.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze", params={"key": api_key}, json={"comment": {"text": data["text"]}, "languages": ["en"], "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}}, "doNotStore": True}, timeout=30)
    response.raise_for_status()
    spans = []
    for name, score in response.json().get("attributeScores", {}).items():
        span_scores = score.get("spanScores", [])
        for span in span_scores:
            spans.append({"start": span.get("begin", 0), "end": span.get("end", 0), "attribute": name})
    return {"redacted_text": redact_spans(data["text"], spans), "spans": spans}
