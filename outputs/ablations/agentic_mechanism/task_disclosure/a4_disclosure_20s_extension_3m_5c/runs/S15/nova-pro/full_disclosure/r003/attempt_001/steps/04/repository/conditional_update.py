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

if __name__ == '__main__':
    table_name = 'YourTableName'
    key = {'id': 'YourPrimaryKey'}
    update_expression = 'SET attribute = :value'
    expression_attribute_values = {':value': 'new_value'}
    expected_version = 1
    response = conditional_update(table_name, key, update_expression, expression_attribute_values, expected_version)
    print(response)