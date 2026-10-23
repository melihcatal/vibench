import os
from google.cloud import aiplatform

def script_embedding(payload, config=None):
    config = config or {}
    project_id = os.environ.get("GCP_PROJECT_ID") # Or get from config
    location = config.get("location", "us-central1") # Or get from config

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set or not provided in config.")

    aiplatform.init(project=project_id, location=location)

    text = payload["text"]

    # Load the text embedding model
    # Model ID: text-embedding-gecko@001 (or other version as available)
    # Using the higher-level SDK for foundation models
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-gecko@003") # Using a common stable version

    embeddings = model.get_embeddings([text])

    # The get_embeddings method returns a list of TextEmbedding objects,
    # each containing the embedding vector. We extract the values.
    embedding_vectors = [e.values for e in embeddings]

    return {"embeddings": embedding_vectors}
