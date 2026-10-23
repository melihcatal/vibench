import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from.database_client import DatabaseClient
from.database_models import DatabaseModels

class RecordTextSafety:
    def __init__(self):
        self.db_client = DatabaseClient()

    def check_text_safety(self, item_id):
        try:
            item = self.db_client.get_item(item_id)
            normalized_item = DatabaseModels.normalize_item(item)
            name = normalized_item['name']
            if 'unsafe' in name.lower():
                return 'Unsafe content detected'
            else:
                return 'Safe content'
        except exceptions.CosmosHttpResponseError as e:
            print(f'Error checking text safety: {e}')
            raise

def main():
    record_text_safety = RecordTextSafety()
    item_id = '1'
    safety_status = record_text_safety.check_text_safety(item_id)
    print(safety_status)

if __name__ == '__main__':
    main()