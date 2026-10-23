import boto3

def fetch_document(table_name, document_id):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(
        TableName=table_name,
        Key={'id': {'S': document_id}}
    )
    item = response.get('Item')
    if item:
        return item
    else:
        return None

if __name__ == '__main__':
    table_name = 'YourDynamoDBTableName'
    document_id = 'YourDocumentId'
    document = fetch_document(table_name, document_id)
    if document:
        print('Document fetched:', document)
    else:
        print('Document not found')