# platform_output_embedding.py
# Later-step scored file: Embed platform outputs for evaluation or retrieval (Google Gemini embeddings API via Vertex AI)

from google.cloud import generativeai as genai
import os
from typing import List, Dict, Any

# Provider configuration
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/vertex-credentials.json"
os.environ["GOOGLE_CLOUD_PROJECT"] = "my-vertex-project"
os.environ["LOCATION"] = "us-central1"

# ---------------------------------------------------------------------------
# Helper to embed text using Vertex AI Gemini Embeddings model
# ---------------------------------------------------------------------------
def embed_text(texts: List[str]) -> List[Dict[str, Any]]:
    """
    Generate embeddings for a list of text strings using Vertex AI Gemini Embeddings.

    Args:
        texts (List[str]): List of text chunks to embed.

    Returns:
        List[Dict[str, Any]]: Each entry contains 'text' and its 'embedding' (dense vector).
    """
    # Vertex AI provides a dedicated embedding model ID
    embed_model = genai.GenerativeModel('gemini-1.5-flash-embedding')
    # Use generate_content with embed_format set to 'text'
    # Vertex AI embeddings API is exposed via .embed_content method
    response = embed_model.embed_content(texts)
    # The response is a list of EmbeddingResponse objects
    embeddings = []
    for idx, part in enumerate(response):
        embeddings.append({
            "text": texts[idx],
            "embedding": part.embedding.tolist()  # convert to Python list
        })
    return embeddings

# Example usage (uncomment to test)
#if __name__ == "__main__":
#    sample_texts = [
#        "The Earth orbits the Sun.",
#        "Quantum computing leverages superposition."
#    ]
#    print(embed_text(sample_texts))
