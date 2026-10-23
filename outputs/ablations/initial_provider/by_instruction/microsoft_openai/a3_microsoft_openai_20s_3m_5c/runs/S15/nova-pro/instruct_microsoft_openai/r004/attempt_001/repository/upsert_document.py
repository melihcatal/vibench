import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions

class DocumentUpserter:
    def __init__(self):
        self.url = os.getenv('COSMOS_DB_URL')
        self.key = os.getenv('COSMOS_DB_KEY')
        self.client = CosmosClient(self.url, credential=self.key)
        self.database_name = 'ManagedNoSQLStore'
        self.container_name = 'Documents'
        self.database = self.client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)

    def upsert_document(self, document):
        try:
            self.container.upsert_item(body=document)
            print('Document upserted successfully')
        except exceptions.CosmosHttpResponseError as e:
            print(f'Error upserting document: {e}')

if __name__ == '__main__':
    document = {
        'id': 'doc1',
        'content': 'This is a sample document'
    }
    upserter = DocumentUpserter()
    upserter.upsert_document(document)