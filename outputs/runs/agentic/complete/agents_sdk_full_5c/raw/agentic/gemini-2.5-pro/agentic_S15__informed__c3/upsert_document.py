from database_client import get_db_table
from database_models import Document
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upsert_document(document: Document) -> bool:
    """
    Upserts (inserts or replaces) a document in the DynamoDB table.

    Args:
        document: A Document object to be upserted.

    Returns:
        True if the operation was successful, False otherwise.
    """
    try:
        table = get_db_table()
        table.put_item(Item=document.to_dynamodb_item())
        logger.info(f"Successfully upserted document with id: {document.id}")
        return True
    except ClientError as e:
        logger.error(
            "Couldn't upsert document %s. Here's why: %s: %s",
            document.id,
            e.response["Error"]["Code"],
            e.response["Error"]["Message"],
        )
        return False
