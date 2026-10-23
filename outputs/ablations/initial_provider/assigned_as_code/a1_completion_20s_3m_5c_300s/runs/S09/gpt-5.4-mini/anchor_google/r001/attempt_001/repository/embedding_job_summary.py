from embed_batch import embed_batch


def embedding_job_summary(payload, config=None):
    embeddings = embed_batch({"texts": payload["texts"]}, config=config)["embeddings"]
    count = len(embeddings)
    dimensions = len(embeddings[0]) if embeddings else 0
    return {"count": count, "dimensions": dimensions}
