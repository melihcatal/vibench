from datetime import datetime, timedelta

from azure.storage.blob import BlobSasPermissions, generate_blob_sas

from storage_client import storage_account_url


def presigned_download(bucket: str, object_name: str, expires_in_seconds: int = 900) -> str:
    from os import environ

    account_name = environ["AZURE_STORAGE_ACCOUNT_NAME"]
    account_key = environ["AZURE_STORAGE_ACCOUNT_KEY"]
    sas = generate_blob_sas(
        account_name=account_name,
        container_name=bucket,
        blob_name=object_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(seconds=expires_in_seconds),
    )
    return f"{storage_account_url()}/{bucket}/{object_name}?{sas}"
