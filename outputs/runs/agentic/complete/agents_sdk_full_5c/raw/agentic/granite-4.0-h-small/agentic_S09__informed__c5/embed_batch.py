# embed_batch.py
# SAME-SCENARIO
from embeddings_client import get_embed_client
from embeddings_models import normalize_embedding

def embed_batch(texts: list):
    """Generate embeddings for a list of text strings.

    Returns a list of normalized embeddings corresponding to each input text.
    """
    client = get_embed_client()
    response = client.create(
        input=[{"text": t} for t in texts],
        model="text-embedding-ada-002"
    )
    embeddings = [normalize_embedding(item['embedding']) for item in response['data']]
    return embeddings
