from azure.storage.blob import BlobServiceClient

def export_records(records, container_name, config):
    connection_string = config['connection_string']
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    for record in records:
        blob_client = container_client.get_blob_client(record['id'])
        blob_client.upload_blob(record, overwrite=True)