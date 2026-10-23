import os
from azure.data.tables import TableClient

def store_expense_record(expense):
    client = TableClient(
        account_url=os.getenv('TABLE_STORAGE_ACCOUNT_URL'),
        table_name=os.getenv('TABLE_NAME'),
        credential=os.getenv('TABLE_STORAGE_ACCOUNT_KEY')
    )
    client.create_entity(expense)