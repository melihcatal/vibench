import os
from datetime import datetime, timedelta

from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

from storage_client import get_blob_service_client, get_blob_client
from storage_models import UploadObjectRequest, UploadObjectResponse

def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    blob_client = get_blob_client(request.container_name, request.blob_name)
    blob_client.upload_blob(request.data, overwrite=True, content_settings={'content_type': request.content_type})

    # Generate a URL for the uploaded blob (can be a public URL or a SAS URL if needed)
    # For simplicity, returning the basic blob URL. For secure access, a SAS token would be appended or generated separately.
    blob_url = blob_client.url

    return UploadObjectResponse(message="Object uploaded successfully", url=blob_url)
