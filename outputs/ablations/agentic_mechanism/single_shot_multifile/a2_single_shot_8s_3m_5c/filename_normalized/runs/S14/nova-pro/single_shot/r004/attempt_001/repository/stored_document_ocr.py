import boto3
from storage_client import get_textract_client

def ocr_document(bucket_name, document_name):
    textract_client = get_textract_client()
    response = textract_client.start_document_text_detection(
        Document={'S3Object':{'Bucket': bucket_name, 'Name': document_name}})
    return response['JobId']

if __name__ == '__main__':
    print(ocr_document('my-bucket','my-document.pdf'))