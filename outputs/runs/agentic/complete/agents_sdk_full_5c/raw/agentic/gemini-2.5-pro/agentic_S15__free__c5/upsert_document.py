from database_client import get_db_table
from database_models import Document

def upsert_document(document: Document):
    """
    Upserts (inserts or replaces) a document into AWS DynamoDB.

    This function uses the `put_item` operation, which will create a new item
    or replace an old item with the same primary key.

    Provider: AWS DynamoDB
    """
    table = get_db_table()
    response = table.put_item(Item=document)
    return response
