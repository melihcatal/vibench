from datetime import datetime, timedelta

from azure.storage.blob import BlobSasPermissions, generate_blob_sas

from storage_client import get_blob_service_client, load_config, normalize_blob_name


def presigned_download(blob_name: str, expires_in_minutes: int = 15, container: str = None) -> str:
    config = load_config(container)
    client = get_blob_service_client(config)
    account_name = client.account_name
    credential = client.credential
    expiry = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    token = generate_blob_sas(account_name=account_name, container_name=config.container, blob_name=normalize_blob_name(blob_name), account_key=getattr(credential, "account_key", None) or credential, permission=BlobSasPermissions(read=True), expiry=expiry)
    return f"{client.url}/{config.container}/{normalize_blob_name(blob_name)}?{token}"
