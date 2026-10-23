from google.cloud import aiplatform


def embed_caption_chunk(
    text_chunk: str, project_id: str, location: str = "us-central1"
) -> list:
    aiplatform.init(project=project_id, location=location)

    # Use a pre-trained text embedding model
    # Model ID can vary; example using a common text embedding model.
    # Refer to Google Cloud Vertex AI documentation for available model IDs.
    # For example, "text-embedding-004" or "text-multilingual-embedding-002"
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings = model.get_embeddings([text_chunk])

    if embeddings and embeddings[0].values:
        return embeddings[0].values
    return []
