from database_client import get_dynamodb_client
from database_models import denormalize_item

def conditional_update(table_name: str, document_id: str, update_expression: str, expression_attribute_values: dict, condition_expression: str | None = None) -> dict:
    """
    Applies a conditional or version-aware update to one stored document in an AWS DynamoDB table.
    """
    dynamodb = get_dynamodb_client()

    key = denormalize_item({"document_id": document_id})

    # Denormalize attribute values for DynamoDB
    denormalized_values = {}
    for k, v in expression_attribute_values.items():
        if isinstance(v, str):
            denormalized_values[k] = {"S": v}
        elif isinstance(v, (int, float)):
            denormalized_values[k] = {"N": str(v)}
        # Add other types as needed

    update_params = {
        "TableName": table_name,
        "Key": key,
        "UpdateExpression": update_expression,
        "ExpressionAttributeValues": denormalized_values,
        "ReturnValues": "ALL_NEW"
    }

    if condition_expression:
        update_params["ConditionExpression"] = condition_expression

    response = dynamodb.update_item(**update_params)
    return response
