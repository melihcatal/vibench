from azure.storage.blob import BlobServiceClient


def archive_metrics_export(export_path, container_name, connection_string):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=export_path)
    with open(export_path, 'rb') as data:
        blob_client.upload_blob(data, overwrite=True)