import os
from azure.cosmos import CosmosClient, PartitionKey

client = CosmosClient(os.getenv('AZURE_COSMOS_ENDPOINT'), credential=os.getenv('AZURE_COSMOS_KEY'))
database = client.get_database_client('expenseDB')
container = database.get_container_client('expenseContainer')

def store_expense_record(record):
    container.create_item(body=record, partition_key=PartitionKey(record['vendor'])