import boto3

def validate_document_fields(document):
    textract = boto3.client('textract')
    response = textract.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['FORMS'])
    form_data = response['Blocks']
    required_fields = ['Name', 'Address', 'Phone']
    missing_fields = []
    low_confidence_fields = []
    for block in form_data:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = block['Text']
            if key in required_fields:
                value = next(item for item in form_data if item['Id'] == block['Relationships'][0]['Ids'][0])['Text']
                confidence = block['Confidence']
                if confidence < 50:
                    low_confidence_fields.append((key, value, confidence))
                else:
                    required_fields.remove(key)
    missing_fields = required_fields
    return missing_fields, low_confidence_fields
