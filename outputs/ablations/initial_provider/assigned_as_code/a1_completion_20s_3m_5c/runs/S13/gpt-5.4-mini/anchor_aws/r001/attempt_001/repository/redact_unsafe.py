from safety_client import get_comprehend_client
from safety_models import normalize_text


def redact_unsafe(payload, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    text = normalize_text(payload.get("text"))
    response = client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode=config.get("language", "en"))
    redacted = text
    spans = []
    for item in response.get("ResultList", []):
        if item.get("Toxicity", 0) >= config.get("threshold", 0.5):
            spans.append(item.get("Index"))
    if spans:
        redacted = "[REDACTED]"
    return {"text": redacted, "unsafe_spans": spans}
