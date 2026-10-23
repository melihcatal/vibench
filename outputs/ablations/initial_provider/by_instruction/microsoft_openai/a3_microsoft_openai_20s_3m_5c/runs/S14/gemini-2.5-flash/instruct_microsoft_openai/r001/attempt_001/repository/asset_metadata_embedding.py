import os
from openai import AzureOpenAI
from storage_client import AzureBlobStorageClient
from storage_models import AssetMetadataEmbeddingRequest, AssetMetadataEmbeddingResponse, ObjectMetadataRequest, ObjectMetadataResponse
from object_metadata import object_metadata
from azure.core.exceptions import ResourceNotFoundError
from dotenv import load_dotenv

load_dotenv()

def asset_metadata_embedding(request: AssetMetadataEmbeddingRequest) -> AssetMetadataEmbeddingResponse:
    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
    azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    azure_openai_embedding_deployment_name = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")

    if not azure_openai_endpoint or not azure_openai_key or not azure_openai_embedding_deployment_name:
        return AssetMetadataEmbeddingResponse(success=False, error="Azure OpenAI environment variables (ENDPOINT, KEY, EMBEDDING_DEPLOYMENT_NAME) not set.")

    client = AzureOpenAI(
        azure_endpoint = azure_openai_endpoint,
        api_key = azure_openai_key,
        api_version = azure_openai_api_version
    )

    try:
        # Get object metadata
        metadata_request = ObjectMetadataRequest(container_name=request.container_name, blob_name=request.blob_name)
        metadata_response = object_metadata(metadata_request)

        if not metadata_response.success:
            return AssetMetadataEmbeddingResponse(success=False, error=f"Failed to retrieve metadata: {metadata_response.error}")

        # Combine relevant metadata and optionally provided text content for embedding
        text_to_embed = f"Blob Name: {metadata_response.name}. "
        if metadata_response.content_settings and metadata_response.content_settings.get("content_type"):
            text_to_embed += f"Content Type: {metadata_response.content_settings['content_type']}. "
        if metadata_response.metadata:
            for k, v in metadata_response.metadata.items():
                text_to_embed += f"{k}: {v}. "
        if request.text_content:
            text_to_embed += f"Document Content: {request.text_content}"
        
        if not text_to_embed.strip():
            return AssetMetadataEmbeddingResponse(success=False, error="No text content or metadata to embed.")

        response = client.embeddings.create(
            input=text_to_embed,
            model=azure_openai_embedding_deployment_name
        )

        embedding = response.data[0].embedding
        return AssetMetadataEmbeddingResponse(success=True, embedding=embedding)

    except ResourceNotFoundError:
        return AssetMetadataEmbeddingResponse(success=False, error=f"Blob '{request.blob_name}' not found in container '{request.container_name}'.")
    except Exception as e:
        return AssetMetadataEmbeddingResponse(success=False, error=str(e))
