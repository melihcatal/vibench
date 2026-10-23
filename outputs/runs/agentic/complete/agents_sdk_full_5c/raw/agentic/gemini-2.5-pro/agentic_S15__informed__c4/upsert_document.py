from database_client import get_db_table
from database_models import Document
from botocore.exceptions import ClientError

def upsert_document(table_name: str, document: Document) -> dict:
    """
    Upserts a document into a specified Amazon DynamoDB table.

    :param table_name: The name of the DynamoDB table.
    :param document: The Document object to upsert.
    :return: The response from the DynamoDB put_item call.
    """
    table = get_db_table(table_name)
    if not table:
        raise ConnectionError("Could not connect to the database.")

    try:
        response = table.put_item(
            Item=document.model_dump()
        )
        return response
    except ClientError as e:
        print(f"Error upserting document {document.id}: {e.response['Error']['Message']}")
        raise
