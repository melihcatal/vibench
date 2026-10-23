import boto3

def fetch_document(table_name, document_id):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(
        TableName=table_name,
        Key={'id': {'S': document_id}}
    )
    return response.get('Item', None)

if __name__ == '__main__':
    table_name = 'YourTableName'
    document_id = 'YourDocumentId'
    document = fetch_document(table_name, document_id)
    print(document)