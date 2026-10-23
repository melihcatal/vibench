from datetime import datetime, timedelta

from azure.storage.blob import generate_blob_sas, BlobSasPermissions

from storage_client import build_blob_service_client


def presigned_download(payload, config=None):
    config = config or {}
    client = build_blob_service_client(config)
    account_name = client.account_name
    sas = generate_blob_sas(
        account_name=account_name,
        container_name=config['container'],
        blob_name=payload['object_name'],
        account_key=config.get('account_key'),
        credential=config.get('account_key'),
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(seconds=payload.get('expires_in', 3600)),
    )
    return {'url': f"{config['account_url']}/{config['container']}/{payload['object_name']}?{sas}"}
