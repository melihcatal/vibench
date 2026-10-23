import os
from ibm_watsonx_ai.embeddings import EmbeddingsClient
from ibm_watsonx_ai.auth import TokenAuth
import hashlib

def embed_translated_segments(segments):
    """Generate embeddings for translated segments using watsonx.ai embeddings."""
    # Use WATSONX_API_KEY and WATSONX_PROJECT_ID from environment for auth
    auth = TokenAuth(token=os.getenv('WATSONX_API_KEY'))
    client = EmbeddingsClient(auth=auth, project_id=os.getenv('WATSONX_PROJECT_ID'))
    embeddings = {}
    for seg in segments:
        # Create a deterministic identifier for each segment (optional)
        seg_id = hashlib.sha256(seg.encode('utf-8')).hexdigest()
        resp = client.get_embedding(input_text=seg)
        embeddings[seg_id] = resp['embedding']
    return embeddings
