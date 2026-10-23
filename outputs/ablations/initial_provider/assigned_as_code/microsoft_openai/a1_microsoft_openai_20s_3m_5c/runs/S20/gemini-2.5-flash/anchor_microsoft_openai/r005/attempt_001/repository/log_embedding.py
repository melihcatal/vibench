import os
from typing import List
from observability_client import get_azure_openai_client
from observability_models import LogEmbedding


def embed_log_message(log_message: str) -> LogEmbedding:
    azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.environ.get("AZURE_OPENAI_API_KEY")
    azure_openai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")
    azure_openai_embedding_deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-ada-002") # Example embedding model

    if not all([azure_openai_endpoint, azure_openai_key]):
        raise ValueError("Missing Azure OpenAI configuration: endpoint or key.")

    client = get_azure_openai_client(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version=azure_openai_api_version
    )

    response = client.embeddings.create(
        input=log_message,
        model=azure_openai_embedding_deployment_name
    )

    embedding_vector = response.data[0].embedding
    return LogEmbedding(embedding_vector=embedding_vector)
