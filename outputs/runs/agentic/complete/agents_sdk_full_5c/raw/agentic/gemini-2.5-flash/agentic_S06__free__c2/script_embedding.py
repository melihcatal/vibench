from google.cloud import aiplatform
from typing import List

def script_embedding(texts: List[str], project_id: str, location: str = "us-central1") -> List[List[float]]:
    """Generates embeddings for a list of texts using Vertex AI's Text Embeddings API."""
    # Model identifier for text embeddings
    model_id = "textembedding-gecko@001" # A concrete model identifier for text embeddings

    aiplatform.init(project=project_id, location=location)
    
    # The Embedding API requires a list of instances, even for a single text.
    # Each instance has a 'content' field.
    instances = [{'content': text} for text in texts]

    parameters = {"auto_truncate": True}

    # Using the Endpoint for synchronous prediction
    # The endpoint path is usually `projects/PROJECT_ID/locations/LOCATION/publishers/google/models/MODEL_ID`
    # However, aiplatform.models.TextEmbeddingModel.from_pretrained handles this abstraction.
    model = aiplatform.models.TextEmbeddingModel.from_pretrained(model_id)
    
    try:
        embeddings_response = model.predict(instances=instances, parameters=parameters)
        # Extract the embeddings from the response
        embeddings = [embedding.values for embedding in embeddings_response.predictions]
        return embeddings
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        print(f"Ensure Vertex AI API is enabled for project '{project_id}' in location '{location}'.")
        return []

if __name__ == '__main__':
    # Example usage (requires GOOGLE_CLOUD_PROJECT environment variable and Vertex AI API enabled)
    import os
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project_id:
        sample_scripts = [
            "This is the first narration script.",
            "The second script talks about a different topic."
        ]
        print(f"Generating embeddings for project: {project_id}")
        embeddings = script_embedding(sample_scripts, project_id=project_id)
        if embeddings:
            for i, emb in enumerate(embeddings):
                print(f"Embedding for script {i+1} (first 5 values): {emb[:5]}...")
                print(f"Embedding dimension: {len(emb)}")
        else:
            print("Failed to generate embeddings.")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Skipping embedding example.")
