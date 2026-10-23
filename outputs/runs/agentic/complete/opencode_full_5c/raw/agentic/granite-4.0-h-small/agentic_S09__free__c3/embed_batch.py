# embed_batch.py
"""
["SAME-SCENARIO"] This script generates embedding vectors for a batch of text strings using an external provider.
"""

from embeddings_client import DirectEmbeddingsClient
from embeddings_models import EmbedRequest, EmbedResponse


def embed_batch(texts: list[str]) -> list[str]:
    """Generate embeddings for a list of text strings.

    Args:
        texts (list[str]): List of input texts.

    Returns:
        list[str]: List of JSON strings, each representing one embedding response.
    """
    client = DirectEmbeddingsClient()
    request = EmbedRequest(texts=texts)
    response: EmbedResponse = client.embed(request)
    return [emb.vector for emb in response.embeddings]


if __name__ == "__main__":
    import json, sys

    if len(sys.argv) < 2:
        print("Usage: python embed_batch.py <text1> [<text2> ...]")
        sys.exit(1)
    texts = sys.argv[1:]
    embeddings_json = embed_batch(texts)
    print(json.dumps(embeddings_json, indent=2))
