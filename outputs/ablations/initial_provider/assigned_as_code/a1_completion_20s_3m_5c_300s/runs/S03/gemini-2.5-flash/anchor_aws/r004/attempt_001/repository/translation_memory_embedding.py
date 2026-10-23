from google.cloud import aiplatform
import os

def embed_text_for_translation_memory(text_segment: str, project_id: str, location: str = "us-central1") -> list:
    # Initialize Vertex AI
    aiplatform.init(project=project_id, location=location)

    # Use the TextEmbeddingModel to get embeddings
    # Model ID: text-embedding-004 (or other suitable)
    model_id = "text-embedding-004"
    embedding_model = aiplatform.TextEmbeddingModel.from_pretrained(model_id)

    embeddings = embedding_model.get_embeddings([text_segment])
    # The response is a list of Embedding objects, each with a values field.
    # We extract the numerical values.
    return embeddings[0].values
