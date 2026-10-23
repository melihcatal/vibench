import boto3

def fetch_document(table_name, document_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'id': document_id})
    return response.get('Item', None)

if __name__ == '__main__':
    table_name = 'YourDynamoDBTableName'
    document_id = 'YourDocumentId'
    document = fetch_document(table_name, document_id)
    print(document)