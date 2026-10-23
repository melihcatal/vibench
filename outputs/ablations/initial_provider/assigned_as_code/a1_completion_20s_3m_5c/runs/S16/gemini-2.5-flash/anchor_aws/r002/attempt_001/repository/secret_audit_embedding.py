from google.cloud import aiplatform

def embed_audit_notes(text: str, project_id: str, location: str) -> list[float]:
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.predict([text])
    return embeddings[0].values
