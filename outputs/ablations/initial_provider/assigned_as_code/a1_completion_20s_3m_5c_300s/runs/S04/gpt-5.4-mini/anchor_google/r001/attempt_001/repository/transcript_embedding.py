from google.cloud import aiplatform


def transcript_embedding(payload, config=None):
    config = config or {}
    project = payload["project_id"]
    location = payload.get("location", "us-central1")
    aiplatform.init(project=project, location=location)
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings([payload["text"]])
    vectors = [embedding.values for embedding in embeddings]
    return {"status": "COMPLETED", "embeddings": vectors}
