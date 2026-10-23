import os
from azure.cosmos import CosmosClient, PartitionKey
os.environ['AZURE_COSMOS_ENDPOINT'] = 'your_cosmos_db_endpoint'
os.environ['AZURE_COSMOS_KEY'] = 'your_cosmos_db_key'

def store_message(message):
    client = CosmosClient(os.getenv('AZURE_COSMOS_ENDPOINT'), credential=os.getenv('AZURE_COSMOS_KEY'))
    database = client.get_database_client('your_database_name')
    container = database.get_container_client('your_container_name')
    container.create_item(body=message)