import boto3

def query_documents(table_name, key, value):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key(key).eq(value)
    )
    return response['Items']

if __name__ == '__main__':
    table_name = 'your_table_name'
    key = 'your_key'
    value = 'your_value'
    documents = query_documents(table_name, key, value)
    for document in documents:
        print(document)