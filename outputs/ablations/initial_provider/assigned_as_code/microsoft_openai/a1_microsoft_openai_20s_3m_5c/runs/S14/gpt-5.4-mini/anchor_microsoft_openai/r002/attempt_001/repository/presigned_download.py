from azure.storage.blob import BlobClient

from storage_client import build_download_sas, get_config


def presigned_download(payload, config=None):
    config = get_config(config)
    sas_token = build_download_sas(config, payload['object_name'], payload.get('expiry_minutes', 15))
    base_url = payload.get('account_url') or config['account_url']
    blob = BlobClient.from_blob_url(f"{base_url.rstrip('/')}/{config['container']}/{payload['object_name']}")
    return {'download_url': f"{blob.url}?{sas_token}"}
