import boto3
from botocore.exceptions import ClientError

def conditional_update(table_name, key, update_expression, expression_attribute_values, condition_expression):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    try:
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ConditionExpression=condition_expression
        )
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print('Conditional check failed.')
        else:
            print('An error occurred:', e)
        return None

# Example usage:
# conditional_update(
#     'ExampleTable',
#     {'id': '123'},
#     'SET info.title = :val1',
#     {':val1': 'Updated Title'},
#     'attribute_not_exists(info.title)'
# )