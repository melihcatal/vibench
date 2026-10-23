import boto3

def validate_fields(document):
    textract = boto3.client('textract')
    response = textract.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['FORMS'])
    blocks = response['Blocks']
    required_fields = ['vendor', 'date', 'total']
    missing_fields = []
    low_confidence_fields = []
    for block in blocks:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = block['Text'] if 'Text' in block else ''
            if key.lower() in required_fields:
                value = next((child['Text'] for child in block['Relationships'][0]['Ids'] if child['BlockType'] == 'VALUE'), '')
                if not value:
                    missing_fields.append(key)
                elif block['Confidence'] < 70:
                    low_confidence_fields.append(key)
    return missing_fields, low_confidence_fields