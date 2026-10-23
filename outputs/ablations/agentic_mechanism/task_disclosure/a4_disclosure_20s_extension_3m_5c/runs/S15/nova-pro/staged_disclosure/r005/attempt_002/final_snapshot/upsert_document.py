import boto3

def upsert_document(table_name, primary_key, document):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.put_item(
        TableName=table_name,
        Item={
            primary_key: {'S': document[primary_key]},
            'data': {'S': json.dumps(document)}
        }
    )
    return response

if __name__ == '__main__':
    table_name = 'YourDynamoDBTableName'
    primary_key = 'YourPrimaryKey'
    document = {
        'YourPrimaryKey': 'YourPrimaryKeyValue',
        'other_field': 'other_value'
    }
    response = upsert_document(table_name, primary_key, document)
    print(response)