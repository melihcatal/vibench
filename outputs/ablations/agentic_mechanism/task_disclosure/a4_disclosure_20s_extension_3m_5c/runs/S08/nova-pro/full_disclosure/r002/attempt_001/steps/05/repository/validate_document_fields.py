import boto3

def validate_document_fields(document):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['FORMS']
    )
    required_fields = ['vendor', 'date', 'total']
    field_confidence_scores = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = block['Text'].lower()
            if key in required_fields:
                field_confidence_scores[key] = block['Confidence']
    for field in required_fields:
        if field not in field_confidence_scores or field_confidence_scores[field] < 70:
            return False
    return True