import os
from typing import Dict, Any
from model_models import ModelResponse

def platform_output_embedding(response: ModelResponse) -> Dict[str, Any]:
    """Embed platform output using watsonx.ai text embeddings (provider-specific).

    Args:
        response: Model response containing the generated text.

    Returns:
        Dict with 'embedding' (list of floats) and metadata about the embedding call.
    """
    from ibm_watsonx_ai import Embeddings
    embeddings = Embeddings(api_key=os.getenv("WATSONX_API_KEY"), project=os.getenv("WATSONX_PROJECT_ID"))
    embed = embeddings.embed_text(response.output)
    # embed returns a list of floats
    return {
        "embedding": embed,
        "metadata": {
            "service": "watsonx.ai",
            "model": "text-embedding",
            "model_version": "latest",
        },
    }
