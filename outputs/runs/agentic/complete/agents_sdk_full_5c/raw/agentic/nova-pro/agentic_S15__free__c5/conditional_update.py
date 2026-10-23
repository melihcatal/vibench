import os
from azure.cosmos import CosmosClient, exceptions

client = CosmosClient(os.environ['COSMOS_URI'], os.environ['COSMOS_KEY'])
database = client.get_database_client('myDatabase')
container = database.get_container_client('myContainer')

def conditional_update(document_id, update_payload):
    try:
        item = container.read_item(item=document_id, partition_key=document_id)
        updated_item = {**item, **update_payload}
        container.upsert_item(updated_item)
    except exceptions.CosmosHttpResponseError as e:
        print(f'An error occurred: {e}')
