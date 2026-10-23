import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from.database_client import DatabaseClient
from.database_models import DatabaseModels

class RecordSummary:
    def __init__(self):
        self.db_client = DatabaseClient()

    def summarize_record(self, item_id):
        try:
            item = self.db_client.get_item(item_id)
            normalized_item = DatabaseModels.normalize_item(item)
            summary = f"Record ID: {normalized_item['id']}, Name: {normalized_item['name']}, Age: {normalized_item['age']}"
            return summary
        except exceptions.CosmosHttpResponseError as e:
            print(f'Error summarizing record: {e}')
            raise

def main():
    record_summary = RecordSummary()
    item_id = '1'
    summary = record_summary.summarize_record(item_id)
    print(summary)

if __name__ == '__main__':
    main()