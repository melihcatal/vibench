from safety_client import get_comprehend_client
from safety_models import normalize_text_payload


def redact_unsafe(payload, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    normalized = normalize_text_payload(payload)
    text = normalized.get("text", "")
    response = client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode=config.get("language", "en"))
    redacted = text
    spans = []
    for item in response.get("ResultList", []):
        for label in item.get("Labels", []):
            if label.get("Name") and label.get("Score", 0) >= config.get("threshold", 0.5):
                spans.append({"label": label["Name"], "score": label["Score"]})
    if spans:
        redacted = "[REDACTED]"
    return {"text": redacted, "spans": spans}
