import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

def conditional_update(table_name, key, update_expression, expression_attribute_values, condition_expression):
    table = dynamodb.Table(table_name)
    response = table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ConditionExpression=condition_expression
    )
    return response