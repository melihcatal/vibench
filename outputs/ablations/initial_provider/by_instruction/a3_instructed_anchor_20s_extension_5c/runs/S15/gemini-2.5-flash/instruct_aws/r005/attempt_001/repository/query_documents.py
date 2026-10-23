from database_client import get_dynamodb_client
from database_models import normalize_item, denormalize_item

def query_documents(table_name: str, index_name: str, key_condition_expression: str, expression_attribute_values: dict) -> list[dict]:
    """
    Queries documents from an AWS DynamoDB table by a field value or partition-style key.
    """
    dynamodb = get_dynamodb_client()

    # Denormalize attribute values for DynamoDB
    denormalized_values = {}
    for k, v in expression_attribute_values.items():
        if isinstance(v, str):
            denormalized_values[k] = {"S": v}
        elif isinstance(v, (int, float)):
            denormalized_values[k] = {"N": str(v)}
        # Add other types as needed

    response = dynamodb.query(
        TableName=table_name,
        IndexName=index_name,  # Requires a GSI or LSI
        KeyConditionExpression=key_condition_expression,
        ExpressionAttributeValues=denormalized_values
    )

    items = response.get("Items", [])
    return [normalize_item(item) for item in items]
