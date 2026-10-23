import os
from openai import AzureOpenAI
from storage_client import AzureBlobStorageClient
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse
from azure.core.exceptions import ResourceNotFoundError
from dotenv import load_dotenv

load_dotenv()

def stored_asset_summary(request: StoredAssetSummaryRequest) -> StoredAssetSummaryResponse:
    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
    azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    azure_openai_deployment_name = os.getenv("AZURE_OPENAI_SUMMARIZE_DEPLOYMENT_NAME")

    if not azure_openai_endpoint or not azure_openai_key or not azure_openai_deployment_name:
        return StoredAssetSummaryResponse(success=False, error="Azure OpenAI environment variables (ENDPOINT, KEY, SUMMARIZE_DEPLOYMENT_NAME) not set.")

    client = AzureOpenAI(
        azure_endpoint = azure_openai_endpoint,
        api_key = azure_openai_key,
        api_version = azure_openai_api_version
    )

    storage_client = AzureBlobStorageClient()

    try:
        blob_client = storage_client.get_blob_client(request.container_name, request.blob_name)
        downloaded_blob = blob_client.download_blob()
        text_content = downloaded_blob.readall().decode('utf-8')

        if not text_content:
            return StoredAssetSummaryResponse(success=True, summary="No content to summarize.")

        prompt = f"Summarize the following text in {request.max_sentences} sentences:\n\n{text_content}"
        response = client.chat.completions.create(
            model=azure_openai_deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=250 # Adjust as needed for summary length
        )

        summary = response.choices[0].message.content.strip()
        return StoredAssetSummaryResponse(success=True, summary=summary)

    except ResourceNotFoundError:
        return StoredAssetSummaryResponse(success=False, error=f"Blob '{request.blob_name}' not found in container '{request.container_name}'.")
    except Exception as e:
        return StoredAssetSummaryResponse(success=False, error=str(e))
