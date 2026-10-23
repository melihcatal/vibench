import datetime
from azure.storage.blob import BlobSASPermissions, generate_blob_sas
from storage_client import get_blob_service_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse


def create_presigned_download_url(
    request: PresignedDownloadRequest,
) -> PresignedDownloadResponse:
    blob_service_client = get_blob_service_client()

    # Get the container client from the service client
    container_client = blob_service_client.get_container_client(request.container_name)

    # Generate SAS token
    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=request.container_name,
        blob_name=request.blob_name,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSASPermissions(read=True),
        expiry=datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(minutes=request.expiry_minutes),
    )

    # Construct the full URL with SAS token
    blob_url = container_client.get_blob_client(request.blob_name).url
    full_url = f"{blob_url}?{sas_token}"

    return PresignedDownloadResponse(url=full_url)
