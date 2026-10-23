import requests

from safety_client import PERSPECTIVE_API_URL, get_api_key
from safety_models import build_result


def redact_unsafe(text, threshold=0.5, replacement="[REDACTED]"):
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "PROFANITY": {},
            "INSULT": {},
            "THREAT": {},
        },
        "spanAnnotations": True,
    }
    response = requests.post(
        f"{PERSPECTIVE_API_URL}?key={get_api_key()}", json=payload, timeout=30
    )
    response.raise_for_status()
    data = response.json()
    spans = []
    for attr in data.get("spanAnnotations", []):
        for span in attr.get("spans", []):
            if span.get("score", {}).get("value", 0.0) >= threshold:
                spans.append((span.get("begin", 0), span.get("end", 0)))
    redacted = text
    for begin, end in sorted(spans, reverse=True):
        redacted = redacted[:begin] + replacement + redacted[end:]
    return build_result(True, {"spans": float(len(spans))}, ["unsafe_spans"], redacted)
