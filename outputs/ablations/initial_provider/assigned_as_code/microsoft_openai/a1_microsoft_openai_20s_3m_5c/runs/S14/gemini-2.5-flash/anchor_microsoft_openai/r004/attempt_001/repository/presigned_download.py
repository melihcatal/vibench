from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from storage_client import get_blob_service_client


def presigned_download(payload, config=None):
    config = config or {}
    account_url = config['account_url']
    container_name = config['container']
    object_name = payload['object_name']
    expiry_minutes = payload.get('expiry_minutes', 60)

    # Generate SAS token
    sas_token = generate_blob_sas(
        account_name=account_url.split('.')[0].split('//')[1],
        container_name=container_name,
        blob_name=object_name,
        account_key=config['account_key'], # Requires account key for generate_blob_sas
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=expiry_minutes)
    )

    # Construct the full URL with SAS token
    download_url = f"{account_url}/{container_name}/{object_name}?{sas_token}"
    return {'object_name': object_name, 'presigned_url': download_url}
