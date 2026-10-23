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

    def conditional_update(self, item_id, item):
        try:
            self.container.replace_item(item_id, item)
        except exceptions.CosmosHttpResponseError as e:
            print(f'Error updating item: {e}')
            raise

def main():
    db_client = DatabaseClient()
    item_id = '1'
    item = {
        'id': item_id,
        'name': 'Jane Doe',
        'age': 35
    }
    db_client.conditional_update(item_id, item)

if __name__ == '__main__':
    main()