import os
from openai import AzureOpenAI
from document_models import EmbeddingResult
from typing import List

def ocr_embedding(text: str, config=None) -> EmbeddingResult:
    if config is None:
        config = {}

    # Azure OpenAI details
    azure_endpoint = config.get('openai_azure_endpoint') or os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_key = config.get('openai_api_key') or os.environ.get("AZURE_OPENAI_KEY")
    api_version = config.get('openai_api_version') or os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")
    embedding_model_deployment = config.get('openai_embedding_model_deployment') or os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")

    if not all([azure_endpoint, api_key, embedding_model_deployment]):
        raise ValueError("Azure OpenAI endpoint, API key, and embedding model deployment name must be provided.")

    client = AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version
    )

    response = client.embeddings.create(
        input=text,
        model=embedding_model_deployment # deployment name
    )

    embedding: List[float] = response.data[0].embedding

    return EmbeddingResult(embedding=embedding, text=text)
