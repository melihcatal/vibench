from typing import List, Dict, Any
from openai import AzureOpenAI

def embed_moderation_reason(reason_texts: List[str], config: Dict[str, Any] = None) -> List[List[float]]:
    config = config or {}
    # Azure OpenAI Configuration
    # Environment variables should be set for AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION
    # or passed via config. Here we use config for consistency.
    
    client = AzureOpenAI(
        azure_endpoint = config.get("azure_openai_endpoint"),
        api_key = config.get("azure_openai_api_key"),
        api_version = config.get("azure_openai_api_version", "2024-02-01"), # Use a recent stable API version
    )

    # The embedding model deployment name
    embedding_deployment_name = config.get("azure_openai_embedding_deployment_name", "text-embedding-ada-002")

    try:
        response = client.embeddings.create(
            input=reason_texts,
            model=embedding_deployment_name
        )
        return [data.embedding for data in response.data]
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return []
