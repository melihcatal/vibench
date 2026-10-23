import os
import json
from azure.storage.blob import BlobServiceClient


def image_asset_archive(
    image_path: str, analysis: dict, container_name: str = "vision-analysis"
) -> str:
    """
    Archive image-analysis artifacts and derived captions in Azure Blob Storage.
    Returns the blob URL.
    """
    account_url = os.getenv("AZURE_STORAGE_ACCOUNT_URL")
    storage_key = os.getenv("AZURE_STORAGE_KEY")
    if not account_url or not storage_key:
        raise ValueError("Set AZURE_STORAGE_ACCOUNT_URL and AZURE_STORAGE_KEY")

    blob_service_client = BlobServiceClient(
        account_url=account_url, credential=storage_key
    )
    container_client = blob_service_client.get_container_client(container_name)

    analysis_json = json.dumps(analysis, indent=2, default=str)
    blob_name = f"{os.path.splitext(os.path.basename(image_path))[0]}_analysis.json"

    blob_client = container_client.upload_blob(
        name=blob_name, data=analysis_json, overwrite=True
    )

    return blob_client.url
