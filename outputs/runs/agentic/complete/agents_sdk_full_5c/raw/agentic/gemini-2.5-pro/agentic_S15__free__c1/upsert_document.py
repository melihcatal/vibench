from decimal import Decimal
import json
from database_client import get_dynamodb_table

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def upsert_document(document_id: str, data: dict):
    """
    Creates or replaces a document in Amazon DynamoDB.

    Args:
        document_id: The primary identifier for the document.
        data: A dictionary containing the document data.
    """
    table = get_dynamodb_table()

    # DynamoDB doesn't handle floats, so we convert them to Decimals.
    # The Boto3 resource handles this conversion automatically for dicts.
    item_to_upsert = data.copy()
    item_to_upsert['id'] = document_id
    
    # Set an initial version for optimistic locking
    if 'version' not in item_to_upsert:
        item_to_upsert['version'] = 1

    response = table.put_item(
        Item=item_to_upsert
    )
    
    print(f"Successfully upserted document {document_id}.")
    return response
