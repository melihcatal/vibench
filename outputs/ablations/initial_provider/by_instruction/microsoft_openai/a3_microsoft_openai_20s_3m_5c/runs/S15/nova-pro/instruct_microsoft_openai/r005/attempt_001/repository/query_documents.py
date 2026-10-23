import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions

class DatabaseClient:
    def __init__(self):
        self.url = os.getenv('COSMOS_DB_URL')
        self.key = os.getenv('COSMOS_DB_KEY')
        self.client = CosmosClient(self.url, self.key)
        self.database_name = os.getenv('COSMOS_DB_DATABASE')
        self.container_name = os.getenv('COSMOS_DB_CONTAINER')
        self.database = self.client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)

    def query_items(self, query):
        try:
            items = list(self.container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            return items
        except exceptions.CosmosHttpResponseError as e:
            print(f'Error querying items: {e}')
            raise

def main():
    db_client = DatabaseClient()
    query = 'SELECT * FROM c WHERE c.age > 30'
    items = db_client.query_items(query)
    for item in items:
        print(item)

if __name__ == '__main__':
    main()