import os
from google.cloud import aiplatform

def embed_text(project_id: str, location: str, text: str) -> list[float]:
    """
    Generates an embedding vector for a single text string using Vertex AI.
    """
    aiplatform.init(project=project_id, location=location)
    
    # Using the latest generally available text embedding model
    model_name = "text-embedding-004"
    model = aiplatform.get_model_registry().get_model_version(model_name).model

    embeddings = model.predict(instances=[{"content": text}])
    
    if embeddings and embeddings.predictions:
        # Assuming the first prediction contains the embedding vector
        return embeddings.predictions[0]['embeddings']['values']
    return []

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        sample_text = "The quick brown fox jumps over the lazy dog."
        embedding = embed_text(project_id, location, sample_text)
        print(f"Embedding for '{sample_text[:30]}...': {embedding[:10]}...") # Print first 10 dimensions