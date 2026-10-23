import boto3


def conditional_update(table_name, key, update_expression, expression_attribute_values):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ConditionExpression="attribute_exists(#key)",
    )
