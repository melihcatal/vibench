import boto3

dynamodb = boto3.client('dynamodb')

def conditional_update(table_name, key, update_expression, expression_attribute_values, condition_expression):
    response = dynamodb.update_item(
        TableName=table_name,
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ConditionExpression=condition_expression
    )
    return response