import boto3

def summarize_document(document_path):
    textract_client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract_client.analyze_document(
            Document={'Bytes': document.read()},
            FeatureTypes=['TABLES', 'FORMS'])
    text = ''.join([item['Text'] for item in response.get('Blocks') if item['BlockType'] == 'LINE'])
    return text

if __name__ == '__main__':\n    document_path = 'path/to/document.pdf'\n    summary = summarize_document(document_path)\n    print(summary)