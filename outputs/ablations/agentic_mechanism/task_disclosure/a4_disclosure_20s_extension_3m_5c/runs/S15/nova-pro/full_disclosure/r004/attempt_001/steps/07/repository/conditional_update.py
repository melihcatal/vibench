import boto3

dynamodb = boto3.resource('dynamodb')


def conditional_update(table_name, key, update_expression, expression_attribute_values, expected_version):
    table = dynamodb.Table(table_name)
    try:
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            Expected={'version': {'Value': expected_version, 'Exists': True}}
        )
        return response
    except Exception as e:
        print(e)
        return None


# Example usage:
# conditional_update(
#     'ExampleTable',
#     {'id': '123'}, # Key of the item to update
#     'SET info.title = :new_title',
#     {':new_title': 'Updated Title'},
#     1 # Expected version
# )