from typing import Dict, Any
from database_client import get_table
from database_models import prepare_document_for_db

def upsert_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Upserts a document into the DynamoDB table.

    Args:
        document: The document to upsert. Must contain the primary key.

    Returns:
        The response from DynamoDB.
    """
    table = get_table()
    # DynamoDB's put_item is an upsert operation.
    # Convert floats to Decimals for boto3 compatibility.
    item_to_insert = prepare_document_for_db(document)
    response = table.put_item(Item=item_to_insert)
    return response
