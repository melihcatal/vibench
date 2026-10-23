```python
# redact_unsafe.py
# SAME-SCENARIO: Flags or redacts unsafe spans from text

import re
from safety_client import SafetyClient

def redact_unsafe(text: str, thresholds: dict = None) -> dict:
    """Return original text with unsafe spans replaced by [REDACTED].
    
    `thresholds` is a dict mapping provider category IDs to score thresholds.
    If a span's score exceeds its threshold, it is masked.
    """
    client = SafetyClient()
    # Assume provider returns a list of spans: [{'start': int, 'end': int, 'category': str, 'score': float}]
    spans = client.detect_unsafe_spans(text)
    if thresholds is None:
        thresholds = {'toxicity': 0.6, 'hate': 0.7}
    pattern = []
    last_end = 0
    for span in spans:
        if span['score'] > thresholds.get(span['category'], 0.0):
            # Ensure non‑overlapping, sort by start
            start = span['start']
            end = span['end']
            pattern.append((start, end, '[REDACTED]'))
    # Apply non‑overlapping replacements
    pattern.sort()
    new_text = text
    for start, end, repl in pattern:
        new_text = new_text[:start] + repl + new_text[end:]
    return {'original': text, 'redacted': new_text, 'unsafe_spans': spans}
```