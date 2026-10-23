# embed_text.py
"""
["SAME-SCENARIO"] This script generates an embedding vector for a single text string using an external provider.
"""

from embeddings_client import DirectEmbeddingsClient
from embeddings_models import EmbedRequest, EmbedResponse

# Example usage: python embed_text.py "sample text"


def embed_single(text: str) -> str:
    """Generate embedding for a single text string.

    Args:
        text (str): Input text.

    Returns:
        str: JSON string of the embedding response.
    """
    client = DirectEmbeddingsClient()
    request = EmbedRequest(texts=[text])
    response: EmbedResponse = client.embed(request)
    # Return first embedding vector as JSON
    return response.embeddings[0].vector


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python embed_text.py <text>")
        sys.exit(1)
    text = sys.argv[1]
    embedding_json = embed_single(text)
    print(embedding_json)
