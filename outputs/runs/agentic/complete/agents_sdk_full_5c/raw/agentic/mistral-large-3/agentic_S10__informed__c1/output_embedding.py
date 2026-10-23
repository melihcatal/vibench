import os
from typing import List, Optional
from model_client import get_watsonx_client
from ibm_watsonx_ai.foundation_models.embeddings import Embeddings


def embed_output(
    text: str,
    model_id: str = "ibm/slate-125m-english-rtrvr",
    project_id: Optional[str] = None
) -> List[float]:
    """
    Embed model outputs for clustering or retrieval using watsonx.ai Slate embeddings.
    """
    client = get_watsonx_client()
    project_id = project_id or os.getenv("WATSONX_PROJECT_ID")
    if not project_id:
        raise ValueError("WATSONX_PROJECT_ID environment variable must be set")

    embeddings = Embeddings(model_id=model_id, client=client.client)
    response = embeddings.create(input=[text], project_id=project_id)
    return response.result.results[0].embedding