import os
from azure.cosmos import CosmosClient, exceptions

class DatabaseClient:
    def __init__(self):
        self.url = os.getenv('COSMOS_DB_URL')
        self.key = os.getenv('COSMOS_DB_KEY')
        self.client = CosmosClient(self.url, credential=self.key)
        self.database_name = 'ManagedNoSQLStore'
        self.container_name = 'Documents'
        self.database = self.client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)

    @staticmethod
    def normalize_document(document):
        return {
            'id': document.get('id'),
            'content': document.get('content', '')
        }

if __name__ == '__main__':
    pass