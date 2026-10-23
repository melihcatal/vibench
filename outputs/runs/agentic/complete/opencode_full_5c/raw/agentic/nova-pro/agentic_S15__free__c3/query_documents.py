import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-west-2")


def query_documents(table_name, key_condition_expression, expression_attribute_values):
    table = dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression=key_condition_expression,
        ExpressionAttributeValues=expression_attribute_values,
    )
    return response.get("Items")
