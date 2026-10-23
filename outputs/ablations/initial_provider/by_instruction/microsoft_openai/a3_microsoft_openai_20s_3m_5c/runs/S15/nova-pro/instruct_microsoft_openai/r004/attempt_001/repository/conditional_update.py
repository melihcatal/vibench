import os
from azure.cosmos import CosmosClient, exceptions

class DocumentUpdater:
    def __init__(self):
        self.url = os.getenv('COSMOS_DB_URL')
        self.key = os.getenv('COSMOS_DB_KEY')
        self.client = CosmosClient(self.url, credential=self.key)
        self.database_name = 'ManagedNoSQLStore'
        self.container_name = 'Documents'
        self.database = self.client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)

    def update_document(self, document_id, new_content):
        try:
            document = self.container.read_item(item=document_id, partition_key=document_id)
            document['content'] = new_content
            self.container.upsert_item(body=document)
            print('Document updated successfully')
        except exceptions.CosmosHttpResponseError as e:
            print(f'Error updating document: {e}')

if __name__ == '__main__':
    updater = DocumentUpdater()
    updater.update_document('doc1', 'This is the updated content')