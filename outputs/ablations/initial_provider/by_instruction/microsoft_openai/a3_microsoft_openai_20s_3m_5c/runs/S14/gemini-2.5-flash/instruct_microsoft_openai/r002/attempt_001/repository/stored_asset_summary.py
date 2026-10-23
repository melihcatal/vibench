import os
from openai import AzureOpenAI
from storage_client import StorageClient
from azure.core.exceptions import ResourceNotFoundError
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse
from io import BytesIO

def stored_asset_summary(request: StoredAssetSummaryRequest) -> StoredAssetSummaryResponse:
    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

    if not azure_openai_endpoint or not azure_openai_key:
        raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY environment variables must be set for summarization.")

    client = AzureOpenAI(
        azure_endpoint = azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version=azure_openai_api_version
    )

    # First, retrieve the content of the asset from Azure Blob Storage
    storage_service_client = StorageClient().get_blob_service_client()
    blob_client = storage_service_client.get_blob_client(container=request.container_name, blob=request.blob_name)

    try:
        download_stream = blob_client.download_blob()
        # Assuming the content is text-based for summarization
        text_content = download_stream.readall().decode('utf-8')
    except ResourceNotFoundError:
        raise FileNotFoundError(f"Object '{request.blob_name}' not found in container '{request.container_name}'.")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve asset content from storage: {e}")

    # Now, use Azure OpenAI to summarize the content
    try:
        response = client.chat.completions.create(
            model=request.model, # deployment name
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Please summarize the following text:\n\n{text_content}"}
            ]
        )
        summary = response.choices[0].message.content
        return StoredAssetSummaryResponse(summary=summary)
    except Exception as e:
        raise RuntimeError(f"Failed to summarize content using Azure OpenAI: {e}")
