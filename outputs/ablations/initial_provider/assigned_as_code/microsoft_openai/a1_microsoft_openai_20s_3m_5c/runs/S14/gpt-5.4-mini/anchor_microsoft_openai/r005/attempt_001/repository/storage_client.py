import os

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

from storage_models import normalize_config


def load_storage_config(config=None):
    cfg = normalize_config(config)
    if 'account_url' not in cfg and os.getenv('AZURE_STORAGE_ACCOUNT_URL'):
        cfg['account_url'] = os.getenv('AZURE_STORAGE_ACCOUNT_URL')
    if 'container' not in cfg and os.getenv('AZURE_STORAGE_CONTAINER'):
        cfg['container'] = os.getenv('AZURE_STORAGE_CONTAINER')
    return cfg


def blob_service_client(config=None):
    cfg = load_storage_config(config)
    return BlobServiceClient(cfg['account_url'], credential=DefaultAzureCredential())


def presigned_blob_url(config, blob_name, expiry_seconds=3600, permissions='r'):
    cfg = load_storage_config(config)
    account_name = cfg.get('account_name')
    account_key = cfg.get('account_key') or os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
    if account_name and account_key:
        sas = generate_blob_sas(
            account_name=account_name,
            container_name=cfg['container'],
            blob_name=blob_name,
            account_key=account_key,
            permission=BlobSasPermissions(read='r' in permissions),
            expiry=None,
        )
        return f"{cfg['account_url'].rstrip('/')}/{cfg['container']}/{blob_name}?{sas}"
    with blob_service_client(cfg) as client:
        return client.get_blob_client(container=cfg['container'], blob=blob_name).url
