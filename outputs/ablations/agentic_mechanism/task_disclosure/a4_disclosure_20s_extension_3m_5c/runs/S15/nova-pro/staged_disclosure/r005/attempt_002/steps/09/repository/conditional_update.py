import boto3

def conditional_update(table_name, key, update_expression, expression_attribute_values, expected_version):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    response = table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        Expected={'version': {'Value': expected_version, 'Exists': True}}
    )

    return response

# Example usage:
# conditional_update('ExampleTable', {'id': '123'}, 'SET #attr = :val', {':val': 'new_value'}, 1)