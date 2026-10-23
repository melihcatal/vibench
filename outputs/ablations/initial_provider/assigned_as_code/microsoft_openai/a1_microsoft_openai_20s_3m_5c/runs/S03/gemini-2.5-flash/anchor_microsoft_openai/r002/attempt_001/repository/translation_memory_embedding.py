import os
from openai import AzureOpenAI
from typing import List, Dict, Any

# NOTE: This assumes Azure OpenAI Service is configured with an API key and endpoint.
# It also assumes a deployment for embeddings (e.g., 'text-embedding-ada-002') is available.

def embed_translated_segments(segments: List[str], config: Dict[str, Any] = None) -> Dict[str, List[List[float]]]:
    config = config or {}
    azure_openai_key = config.get("azure_openai_api_key") or os.environ.get("AZURE_OPENAI_API_KEY")
    azure_openai_endpoint = config.get("azure_openai_endpoint") or os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_embedding_deployment = config.get("azure_embedding_deployment") or os.environ.get("AZURE_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-ada-002")

    if not azure_openai_key or not azure_openai_endpoint:
        raise ValueError("Azure OpenAI API key and endpoint must be provided or set as environment variables.")

    client = AzureOpenAI(
        api_key=azure_openai_key,
        api_version="2024-02-01",
        azure_endpoint=azure_openai_endpoint
    )

    if not segments:
        return {"embeddings": []}

    response = client.embeddings.create(
        input=segments,
        model=azure_embedding_deployment # Use your deployment name for embeddings
    )

    embeddings = [item.embedding for item in response.data]
    return {"embeddings": embeddings}
