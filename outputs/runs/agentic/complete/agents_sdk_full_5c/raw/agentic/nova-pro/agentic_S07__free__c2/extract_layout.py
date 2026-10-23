import boto3

client = boto3.client('textract')

def extract_layout(document):
    response = client.analyze_document(Document={'Bytes': document}, FeatureTypes=['TABLES', 'FORMS'])
    layout = {
        'blocks': [],
        'lines': [],
        'tables': [],
    }
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            layout['lines'].append(block['Text'])
        elif block['BlockType'] == 'TABLE':
            layout['tables'].append(block)
        elif block['BlockType'] == 'LAYOUT_TEXT':
            layout['blocks'].append(block)
    return layout