import boto3

def summarize_document(document_path):
    textract = boto3.client('textract')
    with open(document_path, 'rb') as document:
        imageBytes = document.read()
    response = textract.analyze_document(Document={'Bytes': imageBytes}, FeatureTypes=['TABLES', 'FORMS'])
    document_text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            document_text += item['Text'] + ' '
    return document_text

if __name__ == '__main__':
    document_path = 'path/to/document.pdf'
    summary = summarize_document(document_path)
    print(summary)