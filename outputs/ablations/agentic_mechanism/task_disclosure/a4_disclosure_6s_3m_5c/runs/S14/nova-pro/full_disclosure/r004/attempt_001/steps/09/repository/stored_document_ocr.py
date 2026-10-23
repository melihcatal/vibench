import boto3

def run_ocr(bucket_name, document_key):
    client = boto3.client('textract')
    response = client.detect_document_text(
        Document={'S3Object':{'Bucket': bucket_name, 'Name': document_key}}
    )
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    return text