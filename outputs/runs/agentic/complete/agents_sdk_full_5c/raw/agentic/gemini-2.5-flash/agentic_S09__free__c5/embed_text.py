import os
from google.cloud import aiplatform

# Initialize Vertex AI client
# This assumes that GOOGLE_APPLICATION_CREDENTIALS is set
# or that gcloud auth application-default login has been run.
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
aiplatform.init(project=PROJECT_ID, location=LOCATION)

def embed_text(text: str) -> list[float]:
    """Generates an embedding vector for a single text string using Vertex AI.

    Args:
        text: The text string to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    model = aiplatform.Endpoint.from_pretrained(
        "text-embedding-gecko@001" # Concrete model identifier
    )
    instances = [
        {"content": text}
    ]
    response = model.predict(instances=instances)
    # The embeddings are typically in response.predictions[0]['embeddings']['values']
    # Adjust based on actual API response structure if needed.
    if response.predictions and response.predictions[0] and 'embeddings' in response.predictions[0]:
        return response.predictions[0]['embeddings']['values']
    return []

if __name__ == '__main__':
    sample_text = "Hello, world! This is a test sentence for embedding."
    embedding = embed_text(sample_text)
    print(f"Embedding for \"{sample_text}\": {embedding[:10]}...") # Print first 10 dimensions
    print(f"Embedding dimension: {len(embedding)}")
