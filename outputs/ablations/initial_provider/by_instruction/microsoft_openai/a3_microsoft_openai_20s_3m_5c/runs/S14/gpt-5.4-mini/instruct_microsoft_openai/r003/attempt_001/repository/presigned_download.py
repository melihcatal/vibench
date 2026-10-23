from datetime import datetime, timedelta

from azure.storage.blob import BlobSasPermissions, generate_blob_sas

from storage_client import get_blob_service_client, get_container_name, load_storage_config
from storage_models import SignedUrlRequest


def presigned_download(request: SignedUrlRequest) -> str:
    cfg = load_storage_config()
    service = get_blob_service_client()
    account_name = service.account_name
    expiry = datetime.utcnow() + timedelta(seconds=request.expires_in_seconds)
    token = generate_blob_sas(
        account_name=account_name,
        container_name=get_container_name(request.container_name),
        blob_name=request.object_name,
        account_key=cfg.credential if cfg.credential and len(cfg.credential) > 20 else None,
        permission=BlobSasPermissions(read=True),
        expiry=expiry,
    )
    return f"{cfg.account_url}/{request.container_name}/{request.object_name}?{token}"
