# [LATER-STEP] platform_output_embedding.py
# Embed watsonx.ai model output using IBM Slate embeddings for evaluation or retrieval

import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.consts import WATSONX_API_KEY, WATSONX_PROJECT_ID
from ibm_watsonx_ai.services import Embedding
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from model_models import NormalizedResponse
from typing import Dict, Any


def embed_output(output: NormalizedResponse) -> NormalizedResponse:
    """Return the original response plus an embedding vector for the generated text."""
    api_key = os.getenv(WATSONX_API_KEY)
    project_id = os.getenv(WATSONX_PROJECT_ID)
    if not api_key or not project_id:
        raise RuntimeError(
            "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
        )

    authenticator = IAMAuthenticator(api_key)
    client = APIClient(authenticator=authenticator, project_id=project_id)
    embed = Embedding(client)

    # Slate embeddings accept a list of texts; we embed the generated text
    response = embed.generate_embedding(
        texts=[output.output_text],
        model_id="slate-125m-english-v1",  # example model; adjust as needed
    ).get_result()

    # The response contains a list of embedding vectors (float lists)
    embedding_vector = response["embeddings"][0]["embedding"]
    new_metadata = output.request_metadata.copy()
    new_metadata["embedding_vector"] = embedding_vector
    return NormalizedResponse(
        output_text=output.output_text,
        raw_response=response,
        request_metadata=new_metadata,
    )
