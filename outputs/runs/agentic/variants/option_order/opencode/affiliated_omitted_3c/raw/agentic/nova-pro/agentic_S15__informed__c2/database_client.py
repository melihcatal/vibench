import os
from azure.cosmos import CosmosClient, PartitionKey

COSMOS_ENDPOINT = os.getenv("AZURE_COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("AZURE_COSMOS_KEY")

client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database_name = "myDatabase"
container_name = "myContainer"
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)
