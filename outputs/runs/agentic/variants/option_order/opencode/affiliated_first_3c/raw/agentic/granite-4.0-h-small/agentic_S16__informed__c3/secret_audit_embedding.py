# secret_audit_embedding.py
# [LATER-STEP]
# Embed secret audit notes for semantic search using IBM Slate Embeddings (watsonx.ai)

import os
import json
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.consts import EmbedModel
from ibm_watsonx_ai.embeddings import EmbeddingRequest
from typing import List, Dict


def embed_audit_notes(audit_notes: List[str]) -> List[Dict[str, Any]]:
    """Convert an array of audit note strings into embedding vectors using IBM Slate model.

    Args:
        audit_notes: List of free‑form audit note texts.

    Returns:
        List of dicts, each containing 'text' and 'embedding' (numpy array).
    """
    # Retrieve credentials
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise RuntimeError(
            "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
        )

    client = APIClient(api_key=api_key, project_id=project_id)
    model = EmbedModel.SLATENG_K_30_2024_03_14

    # Batch embeddings: IBM service allows up to 1000 docs per request (adjust as needed)
    batch_size = 100
    embeddings = []
    for i in range(0, len(audit_notes), batch_size):
        batch = audit_notes[i : i + batch_size]
        request = EmbeddingRequest(model=model, text=batch, input_type="PLAIN_TEXT")
        resp = client.embeddings.create(request)
        batch_embeddings = resp.result.get("result", [])
        # Each entry: {"text":"...", "embedding": [0.1,0.2,...]}
        embeddings.extend(batch_embeddings)
    return embeddings
