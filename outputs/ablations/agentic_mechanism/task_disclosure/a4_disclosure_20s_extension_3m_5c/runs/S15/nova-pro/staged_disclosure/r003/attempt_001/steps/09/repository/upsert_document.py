import boto3

def upsert_document(table_name, item):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.put_item(Item=item)
    return response

if __name__ == '__main__':
    table_name = 'YourDynamoDBTableName'
    item = {
        'id': 'primary_identifier',
        'data': {
            'key1': 'value1',
            'key2': 'value2'
        }
    }
    response = upsert_document(table_name, item)
    print(response)