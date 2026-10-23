from embeddings_client import embed_texts


def embedding_job_summary(texts, model=None):
    response = embed_texts(texts, model=model)
    count = 0
    dimensions = 0
    if hasattr(response, "embeddings"):
        count = len(response.embeddings)
        dimensions = len(response.embeddings[0].values) if response.embeddings else 0
    elif isinstance(response, dict) and "embeddings" in response:
        count = len(response["embeddings"])
        dimensions = len(response["embeddings"][0].get("values", [])) if response["embeddings"] else 0
    return {"provider": "google-genai", "count": count, "dimensions": dimensions}
