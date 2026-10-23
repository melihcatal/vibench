import os
from embeddings_client import get_embedding_client

def check_corpus_safety(text: str) -> bool:
    """Run a corpus text through a safety check using watsonx guardrails as an example provider.",
    client = get_embedding_client()
    # Watsonx guardrails endpoint (provider identified by client)
    resp = client.guardrails.evaluate(text=text)
    # Assume response contains 'safe': true/false
    return resp.get('safe', False)
