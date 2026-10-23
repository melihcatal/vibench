import boto3

def extract_fields(document_text):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Text': document_text},
        FeatureTypes=['FORMS'])
    fields = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = ''
            value = ''
            for relationship in block['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        for child_block in response['Blocks']:
                            if child_block['Id'] == child_id:
                                if child_block['BlockType'] == 'WORD':
                                    if key == '':
                                        key = child_block['Text']
                                    else:
                                        value = child_block['Text']
            if key and value:
                fields[key] = value
    return fields