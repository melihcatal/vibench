# redact_unsafe.py
import os
import json
from safety_client import TextSafetyClient

def redact_unsafe(text: str, thresholds: dict) -> dict:
    """Flags or redacts unsafe spans from the input text.
    Returns a dict containing the original text, a redacted version,
    and a list of detected unsafe spans (start/end offsets and category)."""
    client = TextSafetyClient()
    # First request a full analysis to locate unsafe spans
    payload = {
        "content": text,
        "categories": list(thresholds.keys())
    }
    analysis = client.analyze_content(payload)
    unsafe_spans = []
    for item in analysis.get("results", []):
        cat = item.get("category")
        score = item.get("score")
        if score and score >= thresholds.get(cat, 0):
            # Assume the service also returns span offsets under 'spans' if available
            spans = item.get("spans", [])
            for sp in spans:
                unsafe_spans.append({
                    "category": cat,
                    "start": sp.get("start"),
                    "end": sp.get("end"),
                    "confidence": score
                })
    # Simple redaction: replace unsafe text with '[REDACTED]'
    redacted = text
    for sp in unsafe_spans:
        start = sp["start"]
        end = sp["end"]
        redacted = redacted[:start] + "[REDACTED]" + redacted[end:]
    return {
        "original": text,
        "redacted": redacted,
        "unsafe_spans": unsafe_spans
    }

if __name__ == "__main__":
    # Example usage – requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY env vars
    sample = "You are a terrible person and should die."
    thresholds = {"hate": 0.6, "self_harm": 0.6, "sexual": 0.6, "violence": 0.6}
    print(redact_unsafe(sample, thresholds))