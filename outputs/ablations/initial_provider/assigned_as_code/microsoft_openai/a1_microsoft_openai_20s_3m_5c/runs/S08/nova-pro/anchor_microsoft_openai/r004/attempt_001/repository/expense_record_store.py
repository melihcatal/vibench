import json
from azure.storage.blob import BlobServiceClient


def persist_expense_record(expense, connection_string, container_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_name = f'{expense[