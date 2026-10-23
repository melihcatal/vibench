import boto3

def query_documents(table_name, key, value):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.query(
        TableName=table_name,
        KeyConditionExpression='#key = :value',
        ExpressionAttributeNames={'#key': key},
        ExpressionAttributeValues={':value': {'S': value}}
    )
    return response['Items']

if __name__ == '__main__':
    table_name = 'YourTableName'
    key = 'YourKey'
    value = 'YourValue'
    items = query_documents(table_name, key, value)
    print(items)