from datetime import datetime, timedelta, timezone
from typing import Optional

from azure.storage.blob import BlobSasPermissions, generate_blob_sas

from storage_client import build_blob_service_client, load_storage_config, normalize_container_name


def presigned_download(container_name: Optional[str], blob_name: str, expiry_minutes: int = 15) -> str:
    config = load_storage_config()
    container = normalize_container_name(container_name, config)
    service = build_blob_service_client(config)
    account_name = config.account_name or service.account_name
    expiry = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)
    return generate_blob_sas(
        account_name=account_name,
        container_name=container,
        blob_name=blob_name,
        account_key=config.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=expiry,
    )
