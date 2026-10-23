import os
from openai import AzureOpenAI
from security_models import EmbeddingRequest, EmbeddingResponse

def secret_audit_embedding(payload: dict, config: dict = None) -> dict:
    config = config or {}

    # Azure OpenAI credentials and configuration
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT") or config.get('azure_openai_endpoint')
    api_key = os.environ.get("AZURE_OPENAI_API_KEY") or config.get('azure_openai_api_key')
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION") or config.get('azure_openai_api_version', "2023-05-15")
    embedding_deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT") or config.get('azure_openai_embedding_deployment', "text-embedding-ada-002")

    if not azure_endpoint or not api_key:
        raise ValueError("Azure OpenAI endpoint and API key must be provided or set in environment variables.")

    client = AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version,
    )

    request_payload = EmbeddingRequest(text=payload['text'])

    response = client.embeddings.create(
        input=request_payload.text,
        model=embedding_deployment_name  # This is the deployment name in Azure OpenAI Studio
    )

    embedding = response.data[0].embedding
    embedding_response = EmbeddingResponse(embedding=embedding)

    return {"embedding_result": embedding_response.__dict__}
