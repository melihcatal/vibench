from datetime import timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions

from storage_client import load_storage_config


def presigned_download(payload, config=None):
    resolved = load_storage_config(config)
    sas = generate_blob_sas(
        account_name=resolved['account_url'].split('//', 1)[1].split('.', 1)[0],
        container_name=resolved['container'],
        blob_name=payload['object_name'],
        account_key=resolved.get('account_key'),
        permission=BlobSasPermissions(read=True),
        expiry=payload.get('expires_at') or timedelta(minutes=payload.get('expires_in', 15)),
    )
    return {'download_url': f"{resolved['account_url']}/{resolved['container']}/{payload['object_name']}?{sas}"}
