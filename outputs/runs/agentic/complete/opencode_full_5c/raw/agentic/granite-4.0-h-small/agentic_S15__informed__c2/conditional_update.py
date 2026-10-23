import json


def conditional_update(
    client,
    table_name,
    primary_key_value,
    condition_expression,
    update_expression,
    expression_attribute_values=None,
):
    """Apply a conditional or version-aware update to a DynamoDB document."""
    if expression_attribute_values is None:
        expression_attribute_values = {}
    client.update_item(
        TableName=table_name,
        Key={"id": primary_key_value},
        ConditionExpression=condition_expression,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
    )
