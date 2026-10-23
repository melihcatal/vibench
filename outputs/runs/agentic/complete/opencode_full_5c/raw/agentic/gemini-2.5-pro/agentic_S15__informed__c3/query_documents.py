from database_client import get_db_client, DOCUMENTS_TABLE_NAME


def query_documents(category: str):
    dynamodb = get_db_client()

    response = dynamodb.query(
        TableName=DOCUMENTS_TABLE_NAME,
        KeyConditionExpression="category = :c",
        ExpressionAttributeValues={":c": {"S": category}},
    )
    return response.get("Items", [])
