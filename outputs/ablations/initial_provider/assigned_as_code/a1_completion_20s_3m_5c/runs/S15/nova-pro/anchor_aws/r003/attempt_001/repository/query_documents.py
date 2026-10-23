from.database_client import get_dynamodb_client


def query_documents(field_name, field_value, config=None):
    config = config or {}
    client = get_dynamodb_client(config)
    response = client.query(
        TableName=config["table_name"],
        KeyConditionExpression="#field_name = :field_value",
        ExpressionAttributeNames={"#field_name": field_name},
        ExpressionAttributeValues={":field_value": {"S": field_value}}
    )
    items = response.get("Items", [])
    return [item for item in items]