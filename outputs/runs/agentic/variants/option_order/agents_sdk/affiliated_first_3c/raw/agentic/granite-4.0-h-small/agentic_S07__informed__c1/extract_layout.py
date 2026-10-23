import boto3

# Amazon Textract SDK integration for layout extraction
client = boto3.client('textract')

def extract_layout_elements(image_bytes):
    '''Extract layout elements (blocks, lines, key-value sets, tables) from a document using Amazon Textract.'''
    response = client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS', 'TABLES']
    )
    layout = {'blocks': [], 'lines': [], 'tables': [], 'key_values': []}
    for block in response['Blocks']:
        block_id = block['Id']
        if block['BlockType'] == 'PAGE':
            continue
        if block['BlockType'] == 'LINE':
            layout['lines'].append(block['Text'])
        elif block['BlockType'] == 'KEY_VALUE_SET':
            role = block.get('KeyValueSetRole')
            layout['key_values'].append({role: block['Text']})
        elif block['BlockType'] == 'TABLE':
            rows = []
            for relationship in block.get('Relationships', []):
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        child = next((b for b in response['Blocks'] if b['Id'] == child_id), None)
                        if child and child['BlockType'] == 'CELL':
                            rows.append(child['Text'])
            layout['tables'].append(rows)
        else:
            layout['blocks'].append(block['Text'])
    return layout
