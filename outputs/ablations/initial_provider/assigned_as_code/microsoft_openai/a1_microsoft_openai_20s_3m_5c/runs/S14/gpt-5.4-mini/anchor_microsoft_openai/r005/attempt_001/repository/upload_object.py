from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContentSettings


def upload_object(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with BlobServiceClient(config['account_url'], credential=credential) as client:
            blob = client.get_blob_client(container=config['container'], blob=payload['object_name'])
            blob.upload_blob(payload['data'], overwrite=True,
                content_settings=ContentSettings(content_type=payload.get('content_type', 'application/octet-stream')))
    return {'object_name': payload['object_name']}
