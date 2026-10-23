from azure.storage.blob import BlobServiceClient


def export_record_to_archive(record, config):
    blob_service_client = BlobServiceClient(account_url=config['storage_account_url'], credential=config['storage_account_key'])
    blob_client = blob_service_client.get_blob_client(container=config['container_name'], blob=record['id'])
    blob_client.upload_blob(record, overwrite=True)