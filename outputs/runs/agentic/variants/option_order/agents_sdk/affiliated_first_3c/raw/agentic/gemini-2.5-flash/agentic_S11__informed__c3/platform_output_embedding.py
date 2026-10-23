import os
from typing import List

# Assuming `model_client` and `model_models` are available in the local environment
from model_client import VertexAIModelClient
from model_models import EmbeddedOutput

def embed_text_output(text: str, project_id: str = None, location: str = "us-central1", model_name: str = "textembedding-gecko@003") -> EmbeddedOutput:
    client = VertexAIModelClient(project_id=project_id, location=location)
    embedding_model = client.get_text_embedding_model(model_name)

    # The TextEmbeddingModel expects a list of texts
    embeddings = embedding_model.get_embeddings([text])

    if embeddings and embeddings[0].values:
        embedding_values = embeddings[0].values
    else:
        embedding_values = [] # Return empty if no embedding generated

    return EmbeddedOutput(
        embedding=embedding_values,
        text=text,
        metadata={
            "model_name": model_name,
            "project_id": client.project_id,
            "location": client.location,
        },
        # The raw response object from get_embeddings is not directly storable as simple dict
        # but for demonstration, we can indicate its presence or details if needed.
        # For simplicity, we're not including the full raw proto object here.
    )

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Warning: GOOGLE_CLOUD_PROJECT environment variable not set. Embeddings might fail without proper authentication.")

    text_to_embed = "The quick brown fox jumps over the lazy dog."
    
    try:
        print(f"\nEmbedding text: '{text_to_embed}'")
        embedding_result = embed_text_output(text_to_embed, project_id=project_id)
        print(f"Text: {embedding_result.text}")
        print(f"Embedding dimension: {len(embedding_result.embedding)}")
        print(f"First 5 embedding values: {embedding_result.embedding[:5]}...")
        print(f"Metadata: {embedding_result.metadata}")
    except Exception as e:
        print(f"An error occurred during embedding: {e}")
        print("Please ensure Google Cloud Project ID is set and Vertex AI API is enabled.")
