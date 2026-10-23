```python
# moderate_text.py
# SAME-SCENARIO: Scores user text for unsafe or policy‑violating content

from safety_client import SafetyClient

def moderate_text(user_text: str, threshold: float = 0.5) -> dict:
    """Return a safety report for a single text.

    The function sends the text to the external provider and returns a
    dictionary with the raw provider result and a boolean `is_unsafe`.
    """
    client = SafetyClient()
    response = client.analyze_text(user_text)
    # Assume provider returns a dict with a `score` field (0‑1)
    is_unsafe = response.get('score', 0.0) >= threshold
    return {
        'raw': response,
        'is_unsafe': is_unsafe,
        'score': response.get('score')
    }
```