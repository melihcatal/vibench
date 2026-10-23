import boto3

def validate_document_fields(document_path):
    textract_client = boto3.client('textract')
    
    with open(document_path, 'rb') as document:
        imageBytes = document.read()
    
    response = textract_client.analyze_document(
        Document={'Bytes': imageBytes},
        FeatureTypes=['FORMS'])
    
    required_fields = ['Name', 'Address', 'Date']
    field_confidence_scores = {}
    
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = ''
            value = ''
            confidence = 0
            
            for child_block_id in block['ChildBlocks']:
                child_block = next(b for b in response['Blocks'] if b['Id'] == child_block_id['ChildId'])
                if child_block['BlockType'] == 'WORD':
                    if child_block['Relationships'][0]['Type'] == 'CHILD':
                        key = child_block['Text']
                    elif child_block['Relationships'][0]['Type'] == 'VALUE':
                        value = child_block['Text']
                        confidence = child_block['Confidence']
            
            if key in required_fields:
                field_confidence_scores[key] = confidence
    
    for field in required_fields:
        if field not in field_confidence_scores or field_confidence_scores[field] < 50:
            return False
    
    return True
