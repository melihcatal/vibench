```python
# moderate_batch.py
# SAME-SCENARIO: Moderates a batch of user messages and returns per‑message decisions

from safety_client import SafetyClient

def moderate_batch(texts: list[str], threshold: float = 0.5) -> list[dict]:
    """Return a list of safety reports for each text.
    
    Each item mirrors the output of moderate_text().
    """
    client = SafetyClient()
    # Bulk API call (provider may support batch processing)
    responses = client.analyze_batch(texts)
    results = []
    for resp in responses:
        is_unsafe = resp.get('score', 0.0) >= threshold
        results.append({
            'raw': resp,
            'is_unsafe': is_unsafe,
            'score': resp.get('score')
        })
    return results
```