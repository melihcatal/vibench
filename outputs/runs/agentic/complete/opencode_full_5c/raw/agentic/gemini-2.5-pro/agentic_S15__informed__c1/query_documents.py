from boto3.dynamodb.conditions import Key
from database_client import get_db_table


def query_documents_by_author(author: str):
    """
    Queries documents by the author field. Assumes a GSI named 'author-index'.

    :param author: The author's name to query for.
    :return: A list of documents by the specified author.
    """
    table = get_db_table()
    response = table.query(
        IndexName="author-index",  # Assuming a Global Secondary Index on the author field
        KeyConditionExpression=Key("author").eq(author),
    )
    return response.get("Items", [])
