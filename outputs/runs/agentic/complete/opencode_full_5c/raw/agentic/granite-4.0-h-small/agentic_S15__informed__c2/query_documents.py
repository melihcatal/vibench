import json


def query_documents(
    client,
    table_name,
    filter_expression,
    expression_attribute_values=None,
    expression_attribute_names=None,
):
    """Query documents in DynamoDB by a field value or partition key."""
    if expression_attribute_values is None:
        expression_attribute_values = {}
    if expression_attribute_names is None:
        expression_attribute_names = {}
    response = client.query(
        TableName=table_name,
        KeyConditionExpression=filter_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames=expression_attribute_names,
    )
    items = response.get("Items", [])
    return items
