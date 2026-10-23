from google.cloud import aiplatform


def embed_script(text: str, project: str, location: str, model_name: str = "text-embedding-004") -> list[float]:
    aiplatform.init(project=project, location=location)
    model = aiplatform.TextEmbeddingModel.from_pretrained(model_name)
    embeddings = model.get_embeddings([text])
    return embeddings[0].values if embeddings else []
