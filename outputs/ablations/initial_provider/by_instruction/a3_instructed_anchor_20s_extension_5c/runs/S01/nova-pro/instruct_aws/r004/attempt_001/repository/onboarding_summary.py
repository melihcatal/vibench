import boto3

def summarize_text(text):
    client = boto3.client('textract')
    response = client.analyze_document(
        Document={'Bytes': text.encode('utf-8')},
        FeatureTypes=['TABLES', 'FORMS']
    )
    return response['Blocks']