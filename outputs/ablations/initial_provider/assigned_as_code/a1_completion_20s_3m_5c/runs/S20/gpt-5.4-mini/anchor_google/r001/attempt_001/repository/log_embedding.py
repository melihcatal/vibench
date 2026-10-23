from vertexai.language_models import TextEmbeddingModel


def log_embedding(payload, config=None):
    model_name = (config or {}).get("model_name", "text-embedding-004")
    model = TextEmbeddingModel.from_pretrained(model_name)
    texts = payload.get("texts") or [payload.get("text", "")]
    embeddings = model.get_embeddings(texts)
    return {"model": model_name, "embeddings": [embedding.values for embedding in embeddings]}
