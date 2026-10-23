import boto3

def stored_document_ocr(bucket: str, key: str) -> str:
    """
    Runs OCR on a stored document in S3 using Amazon Textract.
    """
    textract_client = boto3.client('textract')
    response = textract_client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        }
    )
    text = ''
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text += block['Text'] + '\n'
    return text.strip()