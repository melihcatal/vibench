import os
from azure.storage.blob import BlobServiceClient

client = BlobServiceClient.from_connection_string(
    os.getenv("STORAGE_CONNECTION_STRING")
)


def archive_image(image_path, container_name="image-archive"):
    blob_client = client.get_blob_client(container=container_name, blob=image_path)
    with open(image_path, "rb") as data:
        blob_client.upload_blob(data)
