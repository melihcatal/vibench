from database_client import get_dynamodb_client
from database_models import normalize_response


def query_documents(field_name: str, field_value: str):
    client = get_dynamodb_client()
    response = client.query(
        TableName=DYNAMODB_TABLE_NAME,
        KeyConditionExpression="#field_name = :field_value",
        ExpressionAttributeNames={"#field_name": field_name},
        ExpressionAttributeValues={":field_value": {"S": field_value}},
    )
    return normalize_response(response)
