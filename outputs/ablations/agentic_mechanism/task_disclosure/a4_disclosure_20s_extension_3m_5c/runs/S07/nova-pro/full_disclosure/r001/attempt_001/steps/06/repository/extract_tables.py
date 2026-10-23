import boto3

def extract_tables(document_path):
    client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        imageBytes = document.read()
    response = client.analyze_document(
        Document={'Bytes': imageBytes},
        FeatureTypes=['TABLES'])
    blocks = response['Blocks']
    table_info = {}
    for block in blocks:
        if block['BlockType'] == 'TABLE':
            table_info[block['Id']] = {
                'Row': block['Row'],
                'Column': block['Column'],
                'Text': block['Text']
            }
    return table_info