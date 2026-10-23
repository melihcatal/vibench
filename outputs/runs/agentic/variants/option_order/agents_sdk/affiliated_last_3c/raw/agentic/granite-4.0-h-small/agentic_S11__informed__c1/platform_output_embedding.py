import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationMetadata

def platform_output_embedding(model_output: str, embedding_model_id: str = "text-embedding-ada-002") -> list[float]:
    """
    Generate an embedding vector for model output using a provider embedding service.
    Uses Azure OpenAI embeddings (could be swapped for OpenAI, Cohere, Gemini, etc.).
    Returns a list of floats representing the vector.
    """
    client = ManagedModelClient()
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    key = os.getenv("AZURE_OPENAI_API_KEY")
    if not (endpoint and key):
        raise RuntimeError("Azure OpenAI credentials not configured")
    import requests
    resp = requests.post(
        f"{endpoint}/openai/deployments/{embedding_model_id}/embeddings?api-version=2023-05-15",
        json={"input": model_output},
        headers={"api-key": key},
    )
    resp.raise_for_status()
    embeddings = resp.json()["data"][0]["embedding"]
    return embeddings

# Example usage (uncomment for local test)
# if __name__ == "__main__":
#     txt = "The capital of France is Paris."
#     vec = platform_output_embedding(txt)
#     print("Embedding size:", len(vec))
#     print("First 5 dims:", vec[:5])
