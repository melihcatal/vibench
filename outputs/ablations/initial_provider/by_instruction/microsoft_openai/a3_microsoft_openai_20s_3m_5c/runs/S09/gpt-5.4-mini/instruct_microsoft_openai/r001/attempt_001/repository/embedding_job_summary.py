from embeddings_client import embed_texts


def embedding_job_summary(texts):
    result = embed_texts(texts)
    return {"count": len(result.embeddings), "dimensions": len(result.embeddings[0]) if result.embeddings else 0}
