from transformers import pipeline
import requests
from embeddings_models import normalize_embedding

def corpus_safety(text: str) -> bool:
    """Check corpus text for harmful content using OpenAI Moderation endpoint."""
    # Simple placeholder: use OpenAI moderation if API key present
    try:
        import openai
        resp = openai.Moderation.create(input=text)
        flagged = resp.results[0].flagged
        return not flagged
    except Exception:
        # Fallback: basic length sanity check
        return len(text) < 10000
