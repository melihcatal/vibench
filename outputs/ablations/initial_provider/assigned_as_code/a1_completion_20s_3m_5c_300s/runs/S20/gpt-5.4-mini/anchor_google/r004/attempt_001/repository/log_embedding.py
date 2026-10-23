from google.cloud import aiplatform


def log_embedding(payload, config=None):
    model = aiplatform.textembedding.TextEmbeddingModel.from_pretrained("text-embedding-004")
    texts = payload["texts"]
    embeddings = model.get_embeddings(texts)
    return {"embeddings": [embedding.values for embedding in embeddings]}
