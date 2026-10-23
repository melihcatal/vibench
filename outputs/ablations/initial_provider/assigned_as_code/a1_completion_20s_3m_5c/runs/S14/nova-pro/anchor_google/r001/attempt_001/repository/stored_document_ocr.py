import boto3
import io

def ocr_document(bucket_name, object_name):
    client = boto3.client('textract')
    response = client.detect_document_text(
        Document={'S3Object':{'Bucket': bucket_name, 'Name': object_name}}
    )
    text = ''.join([item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE'])
    return text