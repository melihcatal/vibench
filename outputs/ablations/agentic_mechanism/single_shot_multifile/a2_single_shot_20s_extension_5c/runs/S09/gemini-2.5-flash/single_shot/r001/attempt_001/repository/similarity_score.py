import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import vertexai
from vertexai.language_models import TextEmbeddingModel

def get_embedding_vertexai(text: str) -> list[float]:
    """
    Generates an embedding vector for a single text string using Google Vertex AI.
    """
    try:
        # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or gcloud auth is configured
        vertexai.init(project=os.environ.get("GCP_PROJECT_ID"), location=os.environ.get("GCP_LOCATION", "us-central1"))
        model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
        embeddings = model.get_embeddings([text])
        return embeddings[0].values
    except Exception as e:
        print(f"Error generating embedding with Vertex AI: {e}")
        return []

def compute_cosine_similarity(text1: str, text2: str) -> float:
    """
    Computes cosine similarity between embeddings of two texts using Google Vertex AI
    for embedding generation.
    """
    embedding1 = get_embedding_vertexai(text1)
    embedding2 = get_embedding_vertexai(text2)

    if not embedding1 or not embedding2:
        print("Could not generate embeddings for similarity calculation.")
        return 0.0

    # Reshape for sklearn's cosine_similarity which expects 2D arrays
    vec1 = np.array(embedding1).reshape(1, -1)
    vec2 = np.array(embedding2).reshape(1, -1)

    return cosine_similarity(vec1, vec2)[0][0]
