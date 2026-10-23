import os
from azure.cosmos import CosmosClient, PartitionKey

# Configuration
endpoint = os.getenv('AZURE_COSMOS_ENDPOINT')
key = os.getenv('AZURE_COSMOS_KEY')
database_name = 'audit_db'
container_name = 'audit_container'

# Authenticate
client = CosmosClient(endpoint, key)
database = client.create_database_if_not_exists(id=database_name)
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path='/id')
)

# Store audit record
def store_audit_record(record):
    container.upsert_item(record)