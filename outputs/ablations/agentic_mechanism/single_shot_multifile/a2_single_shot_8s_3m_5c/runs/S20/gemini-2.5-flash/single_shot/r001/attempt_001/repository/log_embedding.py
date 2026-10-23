import os
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel

from observability_client import get_embedding_model

# aiplatform.init(project=os.environ.get("GCP_PROJECT_ID"), location=os.environ.get("GCP_REGION", "us-central1"))

def embed_log_messages(messages: list[str]) -> list[list[float]]:
    model = get_embedding_model(model_name="text-embedding-004") # Using text-embedding-004 model

    # Embed multiple messages in a single API call for efficiency
    embeddings = model.get_embeddings(messages)

    return [embedding.values for embedding in embeddings]

