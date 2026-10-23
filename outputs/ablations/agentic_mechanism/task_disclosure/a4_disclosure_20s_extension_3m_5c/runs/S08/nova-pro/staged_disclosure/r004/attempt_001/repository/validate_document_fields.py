import boto3

def validate_document_fields(document):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['FORMS'])
    form_data = response['Blocks']
    required_fields = ['Name', 'Address', 'Date']
    confidence_threshold = 80
    validation_results = {}
    for block in form_data:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = block['Text'] if 'TEXT' in block else None
            value = block['Text'] if 'TEXT' in block else None
            confidence = block['Confidence']
            if key in required_fields and confidence >= confidence_threshold:
                validation_results[key] = value
    return validation_results