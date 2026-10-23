from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from storage_models import normalize_config, normalize_payload


def list_prefix(payload, config=None):
    cfg = normalize_config(config)
    pl = normalize_payload(payload)
    prefix = pl.get('prefix', '')
    with DefaultAzureCredential() as credential:
        with BlobServiceClient(cfg['account_url'], credential=credential) as client:
            container = client.get_container_client(cfg['container'])
            objects = [b.name for b in container.list_blobs(name_starts_with=prefix)]
    return {'container': cfg['container'], 'prefix': prefix, 'objects': objects}
