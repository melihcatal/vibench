from.database_client import get_dynamodb_client


def conditional_update(document_id, update_expression, expression_attribute_values, config=None):
    config = config or {}
    client = get_dynamodb_client(config)
    response = client.update_item(
        TableName=config["table_name"],
        Key={config.get("key_field", "id"): {"S": document_id}},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW"
    )
    return response.get("Attributes")