from typing import List, Dict, Any
from botocore.exceptions import ClientError
from database_client import get_boto_client, get_table_name

def query_documents_by_author(author: str) -> List[Dict[str, Any]]:
    """
    Queries for documents by a specific author.
    This assumes a Global Secondary Index (GSI) named 'AuthorIndex'
    with 'author' as the partition key.

    :param author: The author to query documents for.
    :return: A list of document items, or an empty list if none are found.
    """
    dynamodb = get_boto_client()
    table_name = get_table_name()

    try:
        response = dynamodb.query(
            TableName=table_name,
            IndexName='AuthorIndex',  # Specify the GSI
            KeyConditionExpression='author = :author_val',
            ExpressionAttributeValues={
                ':author_val': {'S': author}
            }
        )
        items = response.get('Items', [])
        print(f"Found {len(items)} documents for author {author}")
        return items
    except ClientError as e:
        # Handle case where the index might not exist
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Error: GSI 'AuthorIndex' not found on table {table_name}.")
        else:
            print(f"Error querying documents: {e.response['Error']['Message']}")
        return []

