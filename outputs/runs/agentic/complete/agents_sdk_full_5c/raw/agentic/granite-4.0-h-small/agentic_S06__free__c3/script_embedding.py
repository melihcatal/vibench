# script_embedding.py
# [LATER-STEP]
# Embed narration scripts using Google Cloud Vertex AI Embeddings for voice-asset matching.

import os
from google.cloud import aiplatform

# Utility from same-scenario helpers
from speech_client import TextToSpeechClient  # placeholder import for consistency

# Initialize Vertex AI client (uses GOOGLE_APPLICATION_CREDENTIALS)
aiplatform.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location="us-central1")

# Replace with your model ID family; here we use the general text embedding model v1
TEXT_EMBEDDING_MODEL = "textembedding-gecko"

def embed_script(script: str) -> List[float]:
    """Embed a plain text script using Vertex AI Text Embeddings.
    Returns a list of float embedding vectors.
    """
    # Vertex AI endpoint for embeddings
    model = aiplatform.TextEmbeddingModel.from_pretrained(TEXT_EMBEDDING_MODEL)
    embedding = model.embed_content(script)
    # Vertex AI returns numpy array; convert to list of floats for portability
    return embedding.tolist()


def similarity(vec1: List[float], vec2: List[float]) -> float:
    """Compute cosine similarity between two embeddings."""
    import numpy as np
    a = np.array(vec1)
    b = np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
