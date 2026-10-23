from azure.cosmos import CosmosClient, PartitionKey

def conditional_update(database_name, container_name, document_id, update_operations):
    client = CosmosClient('https://<your-cosmosdb-instance>.documents.azure.com:443/', credential='<your-cosmosdb-key>')
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    document = container.read_item(document_id, partition_key=PartitionKey(document_id))
    document.update(update_operations)
    container.upsert_item(document)

if __name__ == '__main__':
    conditional_update('myDatabase', 'myContainer', '123', {'name': 'Jane Doe'})