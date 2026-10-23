from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from storage_models import normalize_config, normalize_payload, object_response


def object_metadata(payload, config=None):
    cfg = normalize_config(config)
    pl = normalize_payload(payload)
    with DefaultAzureCredential() as credential:
        with BlobServiceClient(cfg['account_url'], credential=credential) as client:
            props = client.get_blob_client(container=cfg['container'], blob=pl['object_name']).get_blob_properties()
    return object_response(pl['object_name'], metadata=dict(props.metadata or {}), content_type=props.content_settings.content_type, size=props.size, etag=props.etag)
