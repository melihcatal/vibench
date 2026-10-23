```python
# safety_threshold.py
# SAME-SCENARIO: Applies category thresholds to decide whether to allow text

from safety_client import SafetyClient

def apply_thresholds(text: str, thresholds: dict) -> dict:
    """Return a decision dict based on provider scores vs thresholds.
    
    Returns { 'allow': bool, 'reasons': list } where reasons are
    categories that exceeded their threshold.
    """
    client = SafetyClient()
    response = client.analyze_text(text)
    # Assume response is a dict with keys as category names and float scores
    exceeded = []
    for category, score in response.items():
        if category in thresholds and score >= thresholds[category]:
            exceeded.append(category)
    return {
        'allow': len(exceeded) == 0,
        'reasons': exceeded,
        'raw': response
    }
```