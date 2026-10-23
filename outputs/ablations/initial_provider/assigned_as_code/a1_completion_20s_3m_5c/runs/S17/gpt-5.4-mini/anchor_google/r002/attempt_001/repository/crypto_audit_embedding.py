from google.cloud import aiplatform


def crypto_audit_embedding(payload, config=None):
    config = config or {}
    aiplatform.init(project=config.get("project_id"), location=config.get("location", "us-central1"))
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings([payload["text"]])
    return {"embedding": embeddings[0].values}
