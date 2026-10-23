import openai
from storage_models import ConfigType, PayloadType
import os

def asset_metadata_embedding(payload: PayloadType, config: ConfigType = None) -> PayloadType:
    config = config or {}
    # Azure OpenAI endpoint, key, and deployment name for embeddings from config or environment variables
    azure_endpoint = config.get("azure_openai_endpoint", os.environ.get("AZURE_OPENAI_ENDPOINT"))
    api_key = config.get("azure_openai_key", os.environ.get("AZURE_OPENAI_KEY"))
    api_version = config.get("azure_openai_api_version", os.environ.get("AZURE_OPENAI_API_VERSION", "2023-05-15")) # Example API version
    embedding_deployment_name = config.get("azure_openai_embedding_deployment_name", os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"))

    text_to_embed = payload["text"]

    if not all([azure_endpoint, api_key, embedding_deployment_name, text_to_embed]):
        raise ValueError("Missing required parameters: Azure OpenAI endpoint, key, embedding deployment name, text to embed.")

    # Configure OpenAI for Azure
    openai.api_type = "azure"
    openai.api_base = azure_endpoint
    openai.api_version = api_version
    openai.api_key = api_key

    try:
        response = openai.Embedding.create(
            input=text_to_embed,
            engine=embedding_deployment_name # Use 'engine' for embeddings with Azure OpenAI
        )
        embedding = response['data'][0]['embedding']
    except Exception as e:
        return {"error": f"Azure OpenAI Embedding failed: {str(e)}"}

    return {"embedding": embedding}
