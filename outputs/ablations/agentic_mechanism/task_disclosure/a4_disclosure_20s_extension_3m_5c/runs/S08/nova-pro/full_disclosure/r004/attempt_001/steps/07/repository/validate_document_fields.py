import boto3

def validate_document_fields(document):
    textract = boto3.client('textract')
    response = textract.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['FORMS'])
    blocks = response['Blocks']
    required_fields = ['vendor', 'date', 'total']
    field_confidence = {}
    for block in blocks:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = block['Text'].lower()
            if key in required_fields:
                field_confidence[key] = block['Confidence']
    for field in required_fields:
        if field not in field_confidence or field_confidence[field] < 70:
            return False, f"Missing or low confidence for field: {field}"
    return True, 'All required fields validated successfully'