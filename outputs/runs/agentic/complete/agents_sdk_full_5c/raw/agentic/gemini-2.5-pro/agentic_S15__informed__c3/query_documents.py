from typing import List, Dict, Any
from database_client import get_db_table
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def query_documents_by_author(author: str) -> List[Dict[str, Any]]:
    """
    Queries for documents by a specific author.

    This assumes the table has a Global Secondary Index (GSI) named 'AuthorIndex'
    with 'author' as the partition key.

    Args:
        author: The author's name to query for.

    Returns:
        A list of documents matching the query.
    """
    try:
        table = get_db_table()
        response = table.query(
            IndexName="AuthorIndex",  # Assumes a GSI on the 'author' attribute
            KeyConditionExpression=Key("author").eq(author),
        )
        items = response.get("Items", [])
        logger.info(f"Found {len(items)} documents for author: {author}")
        return items
    except ClientError as e:
        # Handle case where the index doesn't exist or other errors
        if e.response["Error"]["Code"] == "ValidationException":
            logger.error(
                "Query failed. Ensure a GSI named 'AuthorIndex' exists on the table "
                "with 'author' as the partition key."
            )
        else:
            logger.error(
                "Couldn't query for documents by %s. Here's why: %s: %s",
                author,
                e.response["Error"]["Code"],
                e.response["Error"]["Message"],
            )
        return []
