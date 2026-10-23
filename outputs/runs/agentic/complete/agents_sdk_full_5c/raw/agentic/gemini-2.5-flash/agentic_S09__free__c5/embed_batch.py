import os
from google.cloud import aiplatform

# Initialize Vertex AI client
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
aiplatform.init(project=PROJECT_ID, location=LOCATION)

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generates embedding vectors for a batch of text strings using Vertex AI.

    Args:
        texts: A list of text strings to embed.

    Returns:
        A list of lists of floats, where each inner list is an embedding vector.
    """
    model = aiplatform.Endpoint.from_pretrained(
        "text-embedding-gecko@001" # Concrete model identifier
    )
    instances = [{"content": text} for text in texts]
    response = model.predict(instances=instances)

    batch_embeddings = []
    if response.predictions:
        for prediction in response.predictions:
            if 'embeddings' in prediction:
                batch_embeddings.append(prediction['embeddings']['values'])
    return batch_embeddings

if __name__ == '__main__':
    sample_texts = [
        "The quick brown fox jumps over the lazy dog.",
        "A barking dog never bites.",
        "Learning about embeddings is fun and useful."
    ]
    embeddings = embed_batch(sample_texts)
    for i, emb in enumerate(embeddings):
        print(f"Embedding for text {i+1} (first 5 dim): {emb[:5]}...")
        print(f"Dimension: {len(emb)}")
