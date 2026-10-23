import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions

client = CosmosClient(os.environ['COSMOS_URI'], os.environ['COSMOS_KEY'])
database = client.get_database_client('myDatabase')
container = database.get_container_client('myContainer')

def upsert_document(document):
    try:
        container.upsert_item(document)
    except exceptions.CosmosHttpResponseError as e:
        print(f'An error occurred: {e}')
