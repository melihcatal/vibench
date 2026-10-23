# platform_output_embedding.py
# Managed Model Platform Workflow: embed platform model outputs for evaluation
# Provider: IBM Slate embeddings (watsonx.ai)
import os
import ibm_watsonx_ai
from ibm_watsonx_ai.nlp.embeddings import EmbeddingService
from ibm_watsonx_ai.auth import TrustTokenAuth

# Credentials from environment variables
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

embedding_service = EmbeddingService(auth=TrustTokenAuth(bearer_token=WATSONX_API_KEY), project_id=WATSONX_PROJECT_ID)

def embed_text(text: str) -> dict:
    """Generate embeddings for the supplied text using IBM Slate embeddings.

    Returns a dict with fields:
        - 'embedding': list of float values
        - 'model': model identifier used
        - 'input': original text
    """
    resp = embedding_service.generate_embeddings(text=text, model="slate-125m-english-v3")
    # The API returns a list of embedding vectors, each a list of floats
    vec = resp.embeddings[0].embedding  # assuming single input
    return {
        "embedding": vec,
        "model": resp.embeddings[0].model,
        "input": text,
    }

if __name__ == "__main__":
    # Demo embedding
    demo = "The quick brown fox jumps over the lazy dog."
    result = embed_text(demo)
    print(result)
