from typing import Optional, Dict, Any
from database_client import get_db_table
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_document(document_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetches a single document by its ID from DynamoDB.

    Args:
        document_id: The ID of the document to fetch.

    Returns:
        A dictionary representing the document, or None if not found.
    """
    try:
        table = get_db_table()
        response = table.get_item(Key={"id": document_id})
        item = response.get("Item")
        if item:
            logger.info(f"Successfully fetched document with id: {document_id}")
        else:
            logger.warning(f"Document with id: {document_id} not found.")
        return item
    except ClientError as e:
        logger.error(
            "Couldn't fetch document %s. Here's why: %s: %s",
            document_id,
            e.response["Error"]["Code"],
            e.response["Error"]["Message"],
        )
        return None
