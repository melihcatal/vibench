import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from vision_models import ImageAnalysisResult
from typing import Dict, Any
import json


def archive_image_analysis_results(
    image_id: str,
    original_image_data: bytes,
    analysis_results: ImageAnalysisResult,
    translated_alt_text: str | None = None,
    summary_text: str | None = None,
):
    # Connection string for Azure Storage Account
    # AZURE_STORAGE_ACCOUNT_URL and AZURE_STORAGE_KEY are typically used for AzureKeyCredential, but for BlobServiceClient, a connection string is common.
    # Let's construct it from the provided environment variables or use a direct connection string if available.
    account_url = os.environ.get("AZURE_STORAGE_ACCOUNT_URL")
    account_key = os.environ.get("AZURE_STORAGE_KEY")

    if not account_url or not account_key:
        raise ValueError(
            "AZURE_STORAGE_ACCOUNT_URL and AZURE_STORAGE_KEY environment variables must be set."
        )

    # Construct BlobServiceClient using account URL and SAS token or AzureKeyCredential
    # For this example, we assume account_url is in the format https://<account_name>.blob.core.windows.net
    # and we use AzureKeyCredential.
    blob_service_client = BlobServiceClient(
        account_url=account_url, credential=account_key
    )

    container_name = "image-analysis-archives"
    try:
        container_client = blob_service_client.get_container_client(container_name)
        container_client.create_container()
    except Exception as e:
        # Container already exists or other error, ignore if it's just 'already exists'
        pass

    # Archive original image
    original_image_blob_name = f"{image_id}/original_image.jpg"
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=original_image_blob_name
    )
    blob_client.upload_blob(original_image_data, overwrite=True)

    # Archive analysis results (as JSON)
    analysis_results_dict: Dict[str, Any] = analysis_results.to_dict()
    if translated_alt_text:
        analysis_results_dict["translated_alt_text"] = translated_alt_text
    if summary_text:
        analysis_results_dict["summary_text"] = summary_text

    analysis_json_data = json.dumps(analysis_results_dict, indent=2)
    analysis_blob_name = f"{image_id}/analysis_results.json"
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=analysis_blob_name
    )
    blob_client.upload_blob(analysis_json_data.encode("utf-8"), overwrite=True)

    print(
        f"Archived image {image_id} and its analysis results to Azure Blob Storage container {container_name}"
    )
