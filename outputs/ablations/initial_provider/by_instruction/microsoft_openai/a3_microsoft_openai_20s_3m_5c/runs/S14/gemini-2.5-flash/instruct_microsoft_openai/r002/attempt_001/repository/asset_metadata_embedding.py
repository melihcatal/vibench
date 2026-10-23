import os
from openai import AzureOpenAI
from storage_client import StorageClient
from azure.core.exceptions import ResourceNotFoundError
from storage_models import AssetMetadataEmbeddingRequest, AssetMetadataEmbeddingResponse

def asset_metadata_embedding(request: AssetMetadataEmbeddingRequest) -> AssetMetadataEmbeddingResponse:
    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

    if not azure_openai_endpoint or not azure_openai_key:
        raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY environment variables must be set for embeddings.")

    client = AzureOpenAI(
        azure_endpoint = azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version=azure_openai_api_version
    )

    text_to_embed = ""

    # Fetch metadata if needed and combine with provided text_content
    storage_service_client = StorageClient().get_blob_service_client()
    blob_client = storage_service_client.get_blob_client(container=request.container_name, blob=request.blob_name)

    try:
        properties = blob_client.get_blob_properties()
        metadata_str = " ".join([f"{k}:{v}" for k, v in properties.metadata.items()])
        text_to_embed += metadata_str
    except ResourceNotFoundError:
        # It's possible for an object to exist without explicit metadata, or for the request to only rely on text_content
        pass
    except Exception as e:
        # Log or handle unexpected errors during metadata retrieval
        print(f"Warning: Failed to retrieve object metadata for embedding: {e}")

    if request.text_content:
        text_to_embed += (" " + request.text_content) if text_to_embed else request.text_content

    if not text_to_embed.strip():
        raise ValueError("No content or metadata available to generate embedding.")

    try:
        response = client.embeddings.create(
            input=text_to_embed,
            model=request.model # deployment name for embedding model
        )
        embedding = response.data[0].embedding
        return AssetMetadataEmbeddingResponse(embedding=embedding, model=request.model)
    except Exception as e:
        raise RuntimeError(f"Failed to generate embedding using Azure OpenAI: {e}")
