from azure.cosmos import CosmosClient, PartitionKey

def query_documents(database_name, container_name, query):
    client = CosmosClient('https://<your-cosmosdb-instance>.documents.azure.com:443/', credential='<your-cosmosdb-key>')
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    documents = list(container.query_items(
        query=query,
        enable_cross_partition_query=True))
    return documents

if __name__ == '__main__':
    print(query_documents('myDatabase', 'myContainer', 'SELECT * FROM c WHERE c.name = '))