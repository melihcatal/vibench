from safety_client import create_comprehend_client
from safety_models import normalize_text_payload


def redact_unsafe(payload, config=None):
    client = create_comprehend_client(config)
    data = normalize_text_payload(payload)
    text = data.get("text", "")
    response = client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode="en")
    spans = []
    for item in response.get("ResultList", []):
        for label in item.get("Labels", []):
            if label.get("Score", 0) >= data.get("threshold", 0.5):
                spans.append(label.get("Name", "unsafe"))
    redacted = text
    for span in spans:
        redacted = redacted.replace(span, "[REDACTED]")
    return {"redacted_text": redacted, "flags": spans}
