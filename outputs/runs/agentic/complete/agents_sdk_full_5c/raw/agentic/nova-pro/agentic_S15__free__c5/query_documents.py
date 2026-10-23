import os
from azure.cosmos import CosmosClient, exceptions

client = CosmosClient(os.environ['COSMOS_URI'], os.environ['COSMOS_KEY'])
database = client.get_database_client('myDatabase')
container = database.get_container_client('myContainer')

def query_documents(query):
    try:
        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True))
        return items
    except exceptions.CosmosHttpResponseError as e:
        print(f'An error occurred: {e}')
