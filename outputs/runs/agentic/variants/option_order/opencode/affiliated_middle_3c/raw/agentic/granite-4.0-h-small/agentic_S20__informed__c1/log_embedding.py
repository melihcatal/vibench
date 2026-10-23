import os
from ibm_watsonx_ai import WatsonXEmbeddings


def log_embedding(log_entries: list, model_id: str = "ibm/granite-embed-0908") -> list:
    """Embeds selected log messages for semantic retrieval.

    Uses IBM watsonx.ai Embeddings API. Replace with any other provider
    keeping the same signature.

    Args:
        log_entries (list): List of log dicts with a 'text' field.
        model_id (str): Embedding model identifier.

    Returns:
        list: Entries augmented with an 'embedding' vector (list of floats).
    """
    embed_client = WatsonXEmbeddings()
    embedded = []
    for entry in log_entries:
        text = entry.get("text", "")
        if not text:
            embedded.append(entry)
            continue
        resp = embed_client.embed_text(texts=[text], model_id=model_id)
        embedding = resp.result["embeddings"][0]["embedding"]  # list of floats
        entry = entry.copy()
        entry["embedding"] = embedding
        embedded.append(entry)
    return embedded
