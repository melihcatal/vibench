from google.cloud import aiplatform


def secret_audit_embedding(text: str, project: str, location: str = "us-central1"):
    aiplatform.init(project=project, location=location)
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")
    return model.get_embeddings([text])[0].values
