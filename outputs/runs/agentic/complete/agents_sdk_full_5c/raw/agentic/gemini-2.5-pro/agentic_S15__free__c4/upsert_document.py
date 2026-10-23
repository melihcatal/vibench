from database_client import get_table
from database_models import Document

def upsert_document(doc: Document):
    """
    Inserts or replaces a document in Amazon DynamoDB.

    :param doc: The document object to upsert.
    :return: The response from the DynamoDB put_item call.
    """
    table = get_table()
    response = table.put_item(
        Item=doc.model_dump()
    )
    return response
