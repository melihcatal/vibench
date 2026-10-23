import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from.database_client import DatabaseClient
from.database_models import DatabaseModels

class RecordTranslate:
    def __init__(self):
        self.db_client = DatabaseClient()

    def translate_record(self, item_id):
        try:
            item = self.db_client.get_item(item_id)
            normalized_item = DatabaseModels.normalize_item(item)
            name = normalized_item['name']
            translated_name = f"Translated: {name}"
            return translated_name
        except exceptions.CosmosHttpResponseError as e:
            print(f'Error translating record: {e}')
            raise

def main():
    record_translate = RecordTranslate()
    item_id = '1'
    translated_name = record_translate.translate_record(item_id)
    print(translated_name)

if __name__ == '__main__':
    main()