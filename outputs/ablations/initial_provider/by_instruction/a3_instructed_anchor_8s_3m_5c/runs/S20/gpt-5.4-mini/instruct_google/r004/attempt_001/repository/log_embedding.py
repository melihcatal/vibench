from google.cloud import aiplatform


def log_embedding(text: str) -> list[float]:
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
