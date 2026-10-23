import os
from azure.cosmos import CosmosClient, PartitionKey

def store_message_record(record):
    client = CosmosClient(os.getenv('AZURE_COSMOS_DB_ENDPOINT'), credential=os.getenv('AZURE_COSMOS_DB_KEY'))
    database = client.get_database_client('message-audit-store')
    container = database.get_container_client('messages')
    container.create_item(body=record)

if __name__ == '__main__':
    record = {'message_id': '1234567890', 'status': 'success'}
    store_message_record(record)