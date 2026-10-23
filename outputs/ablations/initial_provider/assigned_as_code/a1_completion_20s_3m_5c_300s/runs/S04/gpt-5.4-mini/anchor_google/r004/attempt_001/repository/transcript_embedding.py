from google.cloud import aiplatform


def transcript_embedding(payload, config=None):
    config = config or {}
    aiplatform.init(project=config.get("project_id"), location=config.get("location", "us-central1"))
    model = aiplatform.models.TextEmbeddingModel.from_pretrained("text-embedding-004")
    texts = payload["segments"]
    embeddings = model.get_embeddings(texts)
    return {"embeddings": [embedding.values for embedding in embeddings]}
