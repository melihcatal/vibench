import boto3

def conditional_update(table_name, key, update_expression, expression_attribute_values, expected_version):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    try:
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            Expected={'version': {'Exists': True, 'Value': expected_version}}
        )
        print('Update successful:', response)
    except Exception as e:
        print('Update failed:', e)

# Example usage
conditional_update(
    table_name='ExampleTable',
    key={'id': '123'},
    update_expression='SET info.title = :val1',
    expression_attribute_values={':val1': 'New Title'},
    expected_version=1
)