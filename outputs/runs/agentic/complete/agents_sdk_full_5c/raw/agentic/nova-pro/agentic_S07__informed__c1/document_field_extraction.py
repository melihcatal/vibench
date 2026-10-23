import boto3

def extract_fields(document_text):
    textract = boto3.client('textract')
    response = textract.analyze_document(Document={'Text': document_text}, FeatureTypes=['FORMS'])
    fields = [(block['KeyDetection']['Text'], block['ValueDetection']['Text']) for block in response['Blocks'] if block['BlockType'] == 'KEY_VALUE_SET']
    return fields