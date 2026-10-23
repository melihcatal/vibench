import boto3

def fetch_document(table_name, document_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={'id': document_id}
    )
    return response.get('Item', None)

if __name__ == '__main__':
    table_name = 'Documents'
    document_id = '12345'
    document = fetch_document(table_name, document_id)
    if document:
        print(f'Document found: {document}')
    else:
        print('Document not found.')