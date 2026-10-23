# [LATER-STEP] script_embedding.py
# Embed narration scripts for voice-asset search.

import os
import json
from typing import Dict, Any


def embed_script(script_text: str) -> Dict[str, Any]:
    """Generate an embedding for a script using IBM Slate embeddings API.

    Args:
        script_text (str): Text to embed.

    Returns:
        Dict[str, Any]: Embedding vector and metadata.
    """
    # ---------------------------------------------------
    # Provider: IBM watsonx.ai text embeddings (SDK)
    # ---------------------------------------------------
    from ibm_watsonx_ai.services import Embeddings

    API_KEY = os.getenv("WATSONX_API_KEY")
    PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
    if not all([API_KEY, PROJECT_ID]):
        raise RuntimeError("WATSONX_API_KEY and WATSONX_PROJECT_ID must be set")
    embeddings = Embeddings(api_key=API_KEY, project_id=PROJECT_ID)
    response = embeddings.generate_embeddings(input_text=[script_text])
    # response.embeddings returns a list of embedding objects
    embedding = response.embeddings[0]
    return {
        "embedding": embedding.embedding.tolist(),
        "metadata": {"input_text": script_text, "text_id": embedding.text_id},
    }


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     sample = "The quick brown fox jumps over the lazy dog."
#     vec = embed_script(sample)
#     print('Embedding size:', len(vec['embedding']))
