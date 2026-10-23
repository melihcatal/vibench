import os

from azure.storage.blob import BlobServiceClient

# [LATER-STEP] metrics_export_archive.py


def archive_metric_snapshot(file_path):
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client("metrics-archive", file_path)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)
