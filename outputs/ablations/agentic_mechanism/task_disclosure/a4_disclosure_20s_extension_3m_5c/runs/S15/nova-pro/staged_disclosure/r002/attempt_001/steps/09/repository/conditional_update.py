import boto3

def conditional_update(table_name, key, update_expression, condition_expression, expression_attribute_values):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    try:
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return response
    except Exception as e:
        print(e)
        return None

# Example usage
# conditional_update('ExampleTable', {'id': '123'}, 'SET info.title = :val1', 'attribute_not_exists(info.title)', {':val1': 'New Title'})