from azure.storage.blob import BlobSasPermissions, generate_blob_sas

from storage_models import normalize_config, normalize_payload, object_response


def presigned_download(payload, config=None):
    cfg = normalize_config(config)
    pl = normalize_payload(payload)
    sas = generate_blob_sas(
        account_name=cfg['account_name'],
        container_name=cfg['container'],
        blob_name=pl['object_name'],
        account_key=cfg['account_key'],
        permission=BlobSasPermissions(read=True),
        expiry=pl.get('expires_at'),
    )
    return object_response(pl['object_name'], url=f"{cfg['account_url'].rstrip('/')}/{cfg['container']}/{pl['object_name']}?{sas}")
