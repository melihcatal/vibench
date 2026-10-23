import os
from azure.data.tables import TableClient, TableServiceClient

def store_expense_record(expense):
    service_client = TableServiceClient.from_connection_string(os.getenv('AZURE_TABLE_STORAGE_CONNECTION_STRING'))
    table_client = service_client.get_table_client(table_name='expenses')
    entity = {
        'PartitionKey': 'expense',
        'RowKey': expense['vendor'] + '-' + expense['date'].replace(' ', ''),
        'vendor': expense['vendor'],
        'date': expense['date'],
        'total': expense['total'],
        'items': expense['items']
    }
    table_client.upsert_entity(entity)