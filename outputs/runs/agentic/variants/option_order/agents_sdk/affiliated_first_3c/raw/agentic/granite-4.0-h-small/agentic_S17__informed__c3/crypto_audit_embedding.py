# Embed crypto audit notes for downstream semantic search.
# Uses watsonx.ai text embeddings (IBM Key Management service context).
# Requires WATSONX_API_KEY and WATSONX_PROJECT_ID env vars.

import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.consts import CollectionIdConsts

def embed_audit_note(note: str) -> dict:
    """Create an embedding for a crypto audit note and return the payload.",
    api = APIClient(
        api_key=os.getenv('WATSONX_API_KEY'),
        project_id=os.getenv('WATSONX_PROJECT_ID')
    )
    # Simple embedding call (IBM provides a client for embeddings)
    embedding_resp = api.embeddings.create(
        input_text=note,
        model_id='text-embedding-3-lIg'
    )
    # The response contains the embedding vector and metadata
    return {
        'note': note,
        'embedding': embedding_resp['embedding']
    }
