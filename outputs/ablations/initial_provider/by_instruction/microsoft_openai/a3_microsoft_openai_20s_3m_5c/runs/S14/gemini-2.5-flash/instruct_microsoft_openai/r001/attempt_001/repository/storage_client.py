import os
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from dotenv import load_dotenv

load_dotenv()

class AzureBlobStorageClient:
    def __init__(self):
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not self.connection_string:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable not set.")
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

    def get_blob_client(self, container_name: str, blob_name: str):
        container_client = self.blob_service_client.get_container_client(container_name)
        return container_client.get_blob_client(blob_name)

    def generate_sas_url(self, container_name: str, blob_name: str, expiry_minutes: int) -> str:
        sas_token = generate_blob_sas(
            account_name=self.blob_service_client.account_name,
            container_name=container_name,
            blob_name=blob_name,
            account_key=self.blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(minutes=expiry_minutes)
        )
        return f"https://{self.blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
