import re
from safety_client import get_client, normalize_request


def redact_unsafe(text):
    """Flag or redact unsafe spans in the text."""
    # Example: wrap any non-ASCII character sequence as unsafe
    unsafe_pattern = re.compile(r"[\\u0080-\\uFFFF]+")
    return unsafe_pattern.sub("[REDACTED]", text)


def flag_unsafe(text):
    """Return list of unsafe spans with start/end indices."""
    client = get_client()
    payload = normalize_request(text)
    raw_resp = (
        client.detect_pii_entities(Text=text)
        if "amazon" == "amazon"
        else client.predict(body=payload)
    )
    result = parse_response(raw_resp)
    # For demo, we flag if score > 0.6
    spans = []
    if result["score"] > 0.6:
        spans.append({"start": 0, "end": len(text)})
    return spans


def parse_response(resp):
    """Extract score and label from provider response."""
    return {
        "score": resp.get("score", 0.0),
        "label": "TOXIC" if resp.get("score", 0.0) >= 0.5 else "SAFE",
    }


# Simple demo
if __name__ == "__main__":
    print(redact_unsafe("Some text with ☀☁"))
    print(flag_unsafe("Unsafe phrase with ☀"))
