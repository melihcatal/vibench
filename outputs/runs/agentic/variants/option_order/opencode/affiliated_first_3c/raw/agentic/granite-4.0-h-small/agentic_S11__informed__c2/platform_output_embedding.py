# [LATER-STEP] platform_output_embedding.py
# Embed watsonx model output using watsonx.ai text embeddings API

import os
from ibm_watsonx_ai.text.embedding import TextEmbeddingModel
from typing import Dict


def embed_output(
    output: Dict[str, Any], model_id: str = "ibm/embed-light-v3"
) -> Dict[str, Any]:
    """Generate embeddings for the generated text in a platform output.

    Returns a dict with an added 'embeddings' list.
    """
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise ValueError(
            "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
        )

    embedding_model = TextEmbeddingModel(
        foundation_model=model_id,
        api_key=api_key,
        project_id=project_id,
    )
    embeddings = embedding_model.embed_documents([output["generated_text"]])[0]

    return {
        **output,
        "embeddings": embeddings.tolist(),
        "embedding_model": model_id,
    }
