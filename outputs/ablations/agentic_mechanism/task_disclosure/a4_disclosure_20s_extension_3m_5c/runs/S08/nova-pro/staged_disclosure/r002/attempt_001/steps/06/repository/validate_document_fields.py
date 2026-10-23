import boto3

def validate_document_fields(document):
    textract = boto3.client('textract')
    response = textract.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['FORMS'])
    blocks = response['Blocks']
    required_fields = ['Name', 'Address', 'Date']
    missing_fields = []
    for field in required_fields:
        found = False
        for block in blocks:
            if block['BlockType'] == 'KEY_VALUE_SET':
                if block['Text'] == field:
                    found = True
                    break
        if not found:
            missing_fields.append(field)
    return missing_fields
