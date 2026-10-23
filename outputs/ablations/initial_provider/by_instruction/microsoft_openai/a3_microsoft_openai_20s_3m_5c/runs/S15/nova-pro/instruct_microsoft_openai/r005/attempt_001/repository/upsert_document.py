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

    def upsert_item(self, item):
        try:
            self.container.upsert_item(body=item)
        except exceptions.CosmosHttpResponseError as e:
            print(f'Error upserting item: {e}')
            raise

def main():
    db_client = DatabaseClient()
    item = {
        'id': '1',
        'name': 'John Doe',
        'age': 30
    }
    db_client.upsert_item(item)

if __name__ == '__main__':
    main()