import os
from azure.cosmos import CosmosClient, PartitionKey

AZURE_COSMOS_ENDPOINT = os.getenv('AZURE_COSMOS_ENDPOINT')
AZURE_COSMOS_KEY = os.getenv('AZURE_COSMOS_KEY')

def login_audit_store(audit_record):
    client = CosmosClient(AZURE_COSMOS_ENDPOINT, credential=AZURE_COSMOS_KEY)
    database = client.get_database_client('auditdb')
    container = database.get_container_client('auditcontainer')
    container.create_item(body=audit_record, partition_key=PartitionKey(audit_record['id']))
    return audit_record