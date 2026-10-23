import os
from typing import List, Dict, Any
from google.cloud import aiplatform

def log_embedding(log_messages: List[str], project_id: str, location: str = "us-central1") -> List[Dict[str, Any]]:
    aiplatform.init(project=project_id, location=location)

    # Using a text embedding model
    # Ensure the Vertex AI API is enabled and proper permissions are set.
    try:
        model = aiplatform.get_model_registry().get_latest_model("text-embedding-004")
    except Exception as e:
        print(f"Warning: Could not get text-embedding-004 from model registry. Trying with TextEmbeddingModel. Error: {e}")
        model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings_data = []
    for message in log_messages:
        # The embed method for TextEmbeddingModel takes a list of texts
        response = model.embed(texts=[message])
        if response.embeddings:
            embedding = response.embeddings[0].values
            embeddings_data.append({"message": message, "embedding": embedding})

    return embeddings_data
