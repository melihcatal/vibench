```python
# moderation_reason_embedding.py
# LATER-STEP: Embed moderation rationales for case retrieval

# Placeholder: integrate with an embedding model (e.g., OpenAI, Cohere)
# Demo returns a dummy vector of zeros

def embed_reason(reason: str) -> List[float]:
    """Return a vector representation for a moderation rationale.

    In production replace with a call to your embedding provider.
    """
    print(f"[EMBED] Embedding reason '{reason}' (demo) -> [0.0]*128")
    return [0.0] * 128
```