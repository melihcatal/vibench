from azure.cosmos import CosmosClient, PartitionKey

def fetch_document(database_name, container_name, document_id):
    client = CosmosClient('https://<your-cosmosdb-instance>.documents.azure.com:443/', credential='<your-cosmosdb-key>')
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    document = container.read_item(document_id, partition_key=PartitionKey(document_id))
    return document

if __name__ == '__main__':
    print(fetch_document('myDatabase', 'myContainer', '123'))