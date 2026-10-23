import os
from google.cloud import aiplatform

def embed_batch(project_id: str, location: str, texts: list[str]) -> list[list[float]]:
    """
    Generates embedding vectors for a batch of text strings using Vertex AI.
    """
    aiplatform.init(project=project_id, location=location)

    # Using the latest generally available text embedding model
    model_name = "text-embedding-004"
    model = aiplatform.get_model_registry().get_model_version(model_name).model
    
    instances = [{"content": text} for text in texts]
    embeddings_response = model.predict(instances=instances)
    
    if embeddings_response and embeddings_response.predictions:
        return [pred['embeddings']['values'] for pred in embeddings_response.predictions]
    return []

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        sample_texts = [
            "Hello, world!",
            "How are you doing today?",
            "This is a test sentence for batch embedding."
        ]
        batch_embeddings = embed_batch(project_id, location, sample_texts)
        for i, embedding in enumerate(batch_embeddings):
            print(f"Embedding for '{sample_texts[i][:20]}...': {embedding[:5]}...") # Print first 5 dimensions