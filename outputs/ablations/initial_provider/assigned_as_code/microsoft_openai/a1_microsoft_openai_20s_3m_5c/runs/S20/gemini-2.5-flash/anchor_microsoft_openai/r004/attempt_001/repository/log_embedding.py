import os
from typing import Dict, Any, List
from openai import AzureOpenAI
from observability_models import EmbeddingRequest, EmbeddingResponse

def create_log_embedding(request: EmbeddingRequest, config: Dict[str, Any] = None) -> EmbeddingResponse:
    config = config or {}

    azure_openai_endpoint = config.get('AZURE_OPENAI_ENDPOINT', os.environ.get('AZURE_OPENAI_ENDPOINT'))
    azure_openai_key = config.get('AZURE_OPENAI_KEY', os.environ.get('AZURE_OPENAI_KEY'))
    azure_openai_embedding_deployment_name = config.get('AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME', os.environ.get('AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME'))

    if not all([azure_openai_endpoint, azure_openai_key, azure_openai_embedding_deployment_name]):
        raise ValueError("Azure OpenAI endpoint, key, or embedding deployment name not configured.")

    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version="2024-02-01"
    )

    response = client.embeddings.create(
        model=azure_openai_embedding_deployment_name, # This is the deployment name for your embedding model.
        input=request.text,
    )

    embedding = response.data[0].embedding
    return EmbeddingResponse(embedding=embedding)
