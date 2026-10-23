import os
from azure.cosmos import CosmosClient

# Initialize the Cosmos client
client = CosmosClient(os.environ['AZURE_COSMOS_ENDPOINT'], credential=os.environ['AZURE_COSMOS_KEY'])

# Select the database and container
database_name = 'your_database_name'
container_name = 'your_container_name'
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

# Query documents by a field value
query = 'SELECT * FROM c WHERE c.field = @field'
parameters = [dict(name='@field', value='value')]
items = list(container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))
print(items)