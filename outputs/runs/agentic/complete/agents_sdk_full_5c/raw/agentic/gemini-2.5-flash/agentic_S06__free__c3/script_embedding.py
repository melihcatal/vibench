import os
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel

# Initialize Vertex AI client
# aiplatform.init() # This line should be run once in the application lifecycle

def embed_narration_script(project_id: str, location: str, script_text: str) -> list:
    """
    Embeds narration scripts for voice-asset search using Google Cloud Vertex AI Text Embedding Model.
    """
    aiplatform.init(project=project_id, location=location)

    # Specify the embedding model, e.g., 'text-embedding-004' or 'text-embedding-gecko@003'
    # Ensure this model is available in your specified region.
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    # The model expects a list of texts for embedding
    embeddings = model.get_embeddings([script_text])

    # Extract the embedding vector from the first (and only) text in the list
    if embeddings and embeddings[0].values:
        return embeddings[0].values
    return []

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS, project ID, and location)
    # PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    # LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1") # Choose a region where embedding models are available
    #
    # if PROJECT_ID != "your-gcp-project-id" and LOCATION != "us-central1":
    #     script_content = "The quick brown fox jumps over the lazy dog."
    #     embedding = embed_narration_script(PROJECT_ID, LOCATION, script_content)
    #
    #     print(f"Script: '{script_content}'")
    #     print(f"Embedding (first 5 values): {embedding[:5]}...")
    #     print(f"Embedding dimension: {len(embedding)}")
    pass
