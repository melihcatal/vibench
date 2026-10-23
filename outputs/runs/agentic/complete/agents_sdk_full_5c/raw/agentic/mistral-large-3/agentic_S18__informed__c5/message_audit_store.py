from azure.cosmos import CosmosClient, PartitionKey
import os
from typing import Dict

def store_message_audit(record: Dict) -> str:
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
    key = os.getenv("AZURE_COSMOS_KEY")
    
    client = CosmosClient(endpoint, key)
    database = client.get_database_client("message_audit_db")
    container = database.get_container_client("processed_messages")
    
    response = container.create_item(body=record)
    return response["id"]