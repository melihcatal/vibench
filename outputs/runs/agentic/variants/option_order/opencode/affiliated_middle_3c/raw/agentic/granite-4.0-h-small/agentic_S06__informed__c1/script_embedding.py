import os
import json
import sys
from watsonx.ai import RuntimeServiceClient  # provider: IBM watsonx.ai Embeddings

from speech_client import get_client
from speech_models import normalize_request

# IBM watsonx environment variables
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
if not WATSONX_API_KEY or not WATSONX_PROJECT_ID:
    raise RuntimeError(
        "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
    )

client = RuntimeServiceClient(api_key=WATSONX_API_KEY)


def embed_narration(script_text: str) -> list[float]:
    """Generate a Text Embedding for a narration script using watsonx.ai Text Embeddings.

    Returns a flat list of floats representing the embedding vector.
    """
    # The watsonx SDK expects a payload like:
    # {
    #   "input": "Your text here",
    #   "parameters": {"model_id": "ibm/granite-13b-v2-text-embed"}
    # }
    model_id = "ibm/granite-13b-v2-text-embed"
    payload = client.create_embeddings(input=script_text, model_id=model_id)
    # The return payload structure depends on the service version; typical field is .result.embeddings
    embeddings = payload.result.embeddings[0].embedding  # list of floats
    return embeddings


def search_for_similar(queries: List[str], top_k: int = 5) -> List[dict]:
    """Search an existing knowledge base of voice assets for the most similar embeddings.

    In a full implementation you would have a vector store of saved embeddings; here we
    just demonstrate the call pattern to watsonx embeddings.
    """
    # Assume we have a stored vector `anchor` (not shown) – we embed the query and then
    # use watsonx's similarity search endpoint (placeholder for demo).
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    # For demo we return dummy similarity scores
    return [{"id": f"asset_{i}", "score": 1.0 - i * 0.1} for i in range(1, top_k + 1)]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: script_embedding.py '<script text>'")
        sys.exit(1)
    script = sys.argv[1]
    emb = embed_narration(script)
    print("Embedding vector length:", len(emb))
    print("First 5 dimensions:", emb[:5])
    # Demo search (no real store, just showing request pattern)
    similar = search_for_similar([script], top_k=3)
    print("Similar assets (demo):", similar)
