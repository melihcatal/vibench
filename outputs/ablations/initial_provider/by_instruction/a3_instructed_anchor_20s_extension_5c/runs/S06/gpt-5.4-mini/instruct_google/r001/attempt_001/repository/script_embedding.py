from google.cloud import aiplatform


def embed_script(text: str, project: str, location: str, model: str = "text-embedding-005") -> list[float]:
    aiplatform.init(project=project, location=location)
    endpoint = aiplatform.TextEmbeddingModel.from_pretrained(model)
    embedding = endpoint.get_embeddings([text])[0].values
    return list(embedding)
