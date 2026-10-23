from azure.storage.blob import BlobServiceClient


def archive_image_analysis_artifacts(payload, analysis_results, config=None):
    config = config or {}
    blob_service_client = BlobServiceClient(account_url=config['storage_account_url'], credential=config['storage_account_key'])
    blob_client = blob_service_client.get_blob_client(container=config['container_name'], blob=payload['image_name'])
    blob_client.upload_blob(analysis_results, overwrite=True)