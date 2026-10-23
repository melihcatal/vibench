import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from.database_client import DatabaseClient
from.database_models import DatabaseModels

class RecordExportArchive:
    def __init__(self):
        self.db_client = DatabaseClient()

    def export_record(self, item_id):
        try:
            item = self.db_client.get_item(item_id)
            normalized_item = DatabaseModels.normalize_item(item)
            archive_name = f"archive_{normalized_item['id']}.json"
            with open(archive_name, 'w') as f:
                f.write(str(normalized_item))
            return archive_name
        except exceptions.CosmosHttpResponseError as e:
            print(f'Error exporting record: {e}')
            raise

def main():
    record_export_archive = RecordExportArchive()
    item_id = '1'
    archive_name = record_export_archive.export_record(item_id)
    print(f'Exported record to {archive_name}')

if __name__ == '__main__':
    main()