import boto3

def upsert_document(table_name, primary_key, document):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.put_item(Item=document)
    return response

if __name__ == '__main__':
    table_name = 'YourDynamoDBTableName'
    primary_key = 'YourPrimaryKey'
    document = {
        'YourPrimaryKey': primary_key,
        'OtherField': 'OtherValue'
    }
    response = upsert_document(table_name, primary_key, document)
    print(response)