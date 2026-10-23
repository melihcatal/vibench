from google.cloud import aiplatform
import os

def embed_log_message(project_id: str, location: str, log_message: str) -> list[float]:
    # Initialize the AI Platform client
    aiplatform.init(project=project_id, location=location)

    # Use the embedding-001 model for text embeddings
    model_name = "textembedding-gecko@003" # Using textembedding-gecko@003 as a common embedding model
    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained(model_name)

    embeddings = model.get_embeddings([log_message])

    # The result is a list of Embedding objects, each containing a list of float values
    # We expect one embedding for one log message, so we take the first one.
    if embeddings:
        return embeddings[0].values
    else:
        return []

