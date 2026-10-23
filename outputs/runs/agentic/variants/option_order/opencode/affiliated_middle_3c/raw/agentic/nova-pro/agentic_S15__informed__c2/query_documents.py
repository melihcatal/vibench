import boto3

AWS_ACCESS_KEY_ID = "your_access_key_id"
AWS_SECRET_ACCESS_KEY = "your_secret_access_key"

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def query_documents(table_name, key_condition_expression, expression_attribute_values):
    table = dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression=key_condition_expression,
        ExpressionAttributeValues=expression_attribute_values,
    )
    return response.get("Items")
