from azure.cosmos import CosmosClient, PartitionKey

def upsert_document(database_name, container_name, document):
    client = CosmosClient('https://<your-cosmosdb-instance>.documents.azure.com:443/', credential='<your-cosmosdb-key>')
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    container.upsert_item(document)

if __name__ == '__main__':
    upsert_document('myDatabase', 'myContainer', {'id': '123', 'name': 'John Doe'})