# [LATER-STEP] moderation_reason_embedding.py

import os
from typing import List, Dict

# Using the IBM Slate embeddings service as the concrete embeddings API.
# Authentication via environment variables WATSONX_API_KEY and WATSONX_PROJECT_ID.


def embed_reasons(reasons: List[str]) -> List[Dict[str, Any]]:
    """Embed a list of moderation rationale strings for case retrieval.

    Returns a list of dicts compatible with the host vector store:
    [{"id": <unique-id>, "text": <original>, "embedding": <list[float]>}].
    """
    try:
        from ibm_watsonx_ai.embeddings import Embeddings
    except ImportError:
        raise RuntimeError(
            "IBM watsonx SDK not installed. Run `pip install ibm-watsonx-ai` to enable embeddings."
        )
    client = Embeddings(
        api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
    )
    # Batch embedding up to the model's limit; here we process one at a time for simplicity.
    embeddings = []
    for idx, reason in enumerate(reasons):
        resp = client.embed_text(reason)
        # Expected response shape: {'embedding': [0.1, 0.2, ...]}
        embeddings.append(
            {"id": f"reason_{idx}", "text": reason, "embedding": resp["embedding"]}
        )
    return embeddings
