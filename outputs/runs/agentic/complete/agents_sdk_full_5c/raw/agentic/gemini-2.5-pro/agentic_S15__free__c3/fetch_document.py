from typing import Dict, Any, Optional
from database_client import get_table
from database_models import normalize_document_from_db

def fetch_document(document_id: str, partition_key: str) -> Optional[Dict[str, Any]]:
    """
    Fetches a document by its composite primary key from DynamoDB.

    Args:
        document_id: The sort key of the document.
        partition_key: The partition key of the document.

    Returns:
        The document if found, otherwise None.
    """
    table = get_table()
    
    # Assuming a composite primary key: (partition_key, document_id)
    # The actual key names must match the table's schema.
    # For this example, we'll assume 'partitionKey' and 'documentId'.
    response = table.get_item(
        Key={
            'partitionKey': partition_key,
            'documentId': document_id
        }
    )
    
    item = response.get('Item')
    if item:
        return normalize_document_from_db(item)
    return None
