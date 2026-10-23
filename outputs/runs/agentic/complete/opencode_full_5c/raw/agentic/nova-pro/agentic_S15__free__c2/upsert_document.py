from database_client import get_table
from database_models import Document


def upsert_document(table_name, document):
    table = get_table(table_name)
    table.put_item(Item=document.to_dict())
