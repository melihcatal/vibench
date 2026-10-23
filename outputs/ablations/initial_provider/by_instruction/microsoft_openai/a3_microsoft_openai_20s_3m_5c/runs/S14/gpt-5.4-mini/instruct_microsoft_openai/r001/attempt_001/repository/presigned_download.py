from datetime import datetime, timedelta

from azure.storage.blob import BlobSasPermissions, generate_blob_sas

from storage_client import load_storage_config
from storage_models import PresignedUrlResult


def presigned_download(object_name, expires_in=900):
    config = load_storage_config()
    expiry = datetime.utcnow() + timedelta(seconds=expires_in)
    sas = generate_blob_sas(
        account_name=config.account_url.split("//", 1)[-1].split(".", 1)[0],
        container_name=config.container_name,
        blob_name=object_name,
        account_key=None,
        permission=BlobSasPermissions(read=True),
        expiry=expiry,
    )
    url = f"{config.account_url.rstrip('/')}/{config.container_name}/{object_name.lstrip('/')}?{sas}"
    return PresignedUrlResult(object_name=object_name, url=url, expires_in=expires_in)
