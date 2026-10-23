import os
from azure.cosmos import CosmosClient, exceptions

class DocumentFetcher:
    def __init__(self):
        self.url = os.getenv('COSMOS_DB_URL')
        self.key = os.getenv('COSMOS_DB_KEY')
        self.client = CosmosClient(self.url, credential=self.key)
        self.database_name = 'ManagedNoSQLStore'
        self.container_name = 'Documents'
        self.database = self.client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)

    def fetch_document(self, document_id):
        try:
            document = self.container.read_item(item=document_id, partition_key=document_id)
            print('Document fetched successfully')
            return document
        except exceptions.CosmosHttpResponseError as e:
            print(f'Error fetching document: {e}')
            return None

if __name__ == '__main__':
    fetcher = DocumentFetcher()
    document = fetcher.fetch_document('doc1')