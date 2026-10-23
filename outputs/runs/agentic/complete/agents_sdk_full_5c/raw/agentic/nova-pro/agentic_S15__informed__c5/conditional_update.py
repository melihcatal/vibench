import os
from azure.cosmos import CosmosClient, PartitionKey

# Initialize the Cosmos client
client = CosmosClient(os.environ['AZURE_COSMOS_ENDPOINT'], credential=os.environ['AZURE_COSMOS_KEY'])

# Select the database and container
database_name = 'your_database_name'
container_name = 'your_container_name'
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

# Conditional update
document_id = 'document_id'
document = container.read_item(item=document_id, partition_key=PartitionKey(document_id))
document['field'] = 'new_value'
container.replace_item(item=document['id'], body=document)