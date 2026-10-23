from google.cloud import aiplatform


def script_embedding(payload, config=None):
    config = config or {}
    aiplatform.init(project=config.get("project_id"), location=config.get("location", "us-central1"))
    model = aiplatform.TextEmbeddingModel.from_pretrained(config.get("model_id", "textembedding-gecko@003"))
    embeddings = model.get_embeddings([payload["text"]])
    return {"embedding": embeddings[0].values, "model_id": config.get("model_id", "textembedding-gecko@003")}
