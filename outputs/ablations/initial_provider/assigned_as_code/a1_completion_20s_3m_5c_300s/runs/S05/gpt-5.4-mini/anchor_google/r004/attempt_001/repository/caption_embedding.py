from google.cloud import aiplatform


def caption_embedding(payload, config=None):
    config = config or {}
    aiplatform.init(project=config.get("project_id"), location=config.get("location", "us-central1"))
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings(payload["chunks"])
    vectors = [embedding.values for embedding in embeddings]
    return {"vectors": vectors, "model": "textembedding-gecko@003"}
