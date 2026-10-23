import boto3

def summarize_text(text):
    textract = boto3.client('textract')
    response = textract.analyze_document(Document={'Bytes': text.encode('utf-8')}, FeatureTypes=['TABLES', 'FORMS'])
    blocks = response['Blocks']
    summary = ''
    for block in blocks:
        if block['BlockType'] == 'LINE':
            summary += block['Text'] + ' '
    return summary