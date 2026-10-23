from azure.storage.blob import generate_blob_sas, BlobSasPermissions

from storage_client import load_storage_config
from storage_models import normalize_object_name


def presigned_download(payload, config=None):
    config = load_storage_config(config)
    object_name = normalize_object_name(payload['object_name'])
    sas = generate_blob_sas(
        account_name=config['account_url'].split('//', 1)[-1].split('.', 1)[0],
        container_name=config['container'],
        blob_name=object_name,
        account_key=config.get('account_key'),
        permission=BlobSasPermissions(read=True),
        expiry=payload['expires_at'],
    )
    return {'url': f"{config['account_url']}/{config['container']}/{object_name}?{sas}"}
