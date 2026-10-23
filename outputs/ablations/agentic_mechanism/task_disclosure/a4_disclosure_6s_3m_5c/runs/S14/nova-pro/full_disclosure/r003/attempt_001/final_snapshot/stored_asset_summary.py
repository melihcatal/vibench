import boto3

def summarize_stored_asset(bucket_name, document_name):
    client = boto3.client('textract')
    response = client.analyze_document(
        Document={'S3Object':{'Bucket': bucket_name, 'Name': document_name}},
        FeatureTypes=['TABLES', 'FORMS'])
    # Extract text from the document
    text = ''
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text += block['Text'] + ' '
    # Summarize the extracted text
    summary = text[:200]  # Simple truncation for demonstration
    return summary
