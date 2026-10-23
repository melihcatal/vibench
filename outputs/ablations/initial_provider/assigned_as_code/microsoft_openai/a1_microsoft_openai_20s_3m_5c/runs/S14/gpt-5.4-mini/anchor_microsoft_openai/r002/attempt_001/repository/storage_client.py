from datetime import datetime, timedelta, timezone

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions


def get_config(config=None):
    config = config or {}
    return {
        'account_url': config['account_url'],
        'container': config['container'],
        'account_name': config.get('account_name'),
        'account_key': config.get('account_key'),
        'credential': config.get('credential'),
    }


def get_blob_service_client(config=None):
    config = get_config(config)
    credential = config['credential'] or DefaultAzureCredential()
    return BlobServiceClient(config['account_url'], credential=credential)


def normalize_blob_properties(properties):
    return {
        'content_type': getattr(properties, 'content_settings', None) and properties.content_settings.content_type,
        'content_length': getattr(properties, 'size', None),
        'etag': getattr(properties, 'etag', None),
        'last_modified': getattr(properties, 'last_modified', None),
        'metadata': getattr(properties, 'metadata', None) or {},
    }


def build_download_sas(config, blob_name, expiry_minutes=15):
    config = get_config(config)
    expiry = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)
    return generate_blob_sas(
        account_name=config['account_name'],
        container_name=config['container'],
        blob_name=blob_name,
        account_key=config['account_key'],
        permission=BlobSasPermissions(read=True),
        expiry=expiry,
    )
