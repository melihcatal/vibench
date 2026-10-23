import os
from typing import Dict
from azure.cosmos import CosmosClient, PartitionKey

# Azure Cosmos DB for NoSQL
AZURE_COSMOS_ENDPOINT = os.getenv("AZURE_COSMOS_ENDPOINT")
AZURE_COSMOS_KEY = os.getenv("AZURE_COSMOS_KEY")
AZURE_COSMOS_DATABASE = os.getenv("AZURE_COSMOS_DATABASE", "FederatedLoginAudit")
AZURE_COSMOS_CONTAINER = os.getenv("AZURE_COSMOS_CONTAINER", "AuditRecords")

client = CosmosClient(AZURE_COSMOS_ENDPOINT, AZURE_COSMOS_KEY)
database = client.create_database_if_not_exists(id=AZURE_COSMOS_DATABASE)
container = database.create_container_if_not_exists(
    id=AZURE_COSMOS_CONTAINER, partition_key=PartitionKey(path="/provider")
)

def store_audit_record(record: Dict) -> None:
    container.create_item(body=record)