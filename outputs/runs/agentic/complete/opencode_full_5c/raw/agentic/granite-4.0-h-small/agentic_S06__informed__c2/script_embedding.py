# [LATER-STEP] script_embedding.py
# Embed narration scripts for voice‑asset search using Watsonx.ai embeddings

import os
from ibm_watsonx_ai.api_client import APIClient
from ibm_watsonx_ai.hlp.settings import Settings

# Load credentials via environment variables
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
if not (WATSONX_API_KEY and WATSONX_PROJECT_ID):
    raise RuntimeError(
        "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
    )

# Configure SDK to use Granite embedding model (slate)
Settings.instance().update(
    project_id=WATSONX_PROJECT_ID,
    api_key=WATSONX_API_KEY,
    auth_type="iam",
    service_url="https://us-south.ml.cloud.ibm.com",
)
from ibm_watsonx_ai.nlp.embeddings import SlateEmbeddings

embedder = SlateEmbeddings()


def embed_script(script: str) -> list:
    """Compute a vector embedding for the supplied narration text.

    Args:
        script (str): The narration to embed.

    Returns:
        List[float]: A list of embedding dimensions.
    """
    response = embedder.embed_documents([script])
    # The API returns a list of dicts; extract the 1536‑dim vector
    return response[0]["embedding"]


# Example usage
if __name__ == "__main__":
    sample = "A simple narration about the weather."
    vec = embed_script(sample)
    print("Embedding vector (first 5 dims):", vec[:5])
