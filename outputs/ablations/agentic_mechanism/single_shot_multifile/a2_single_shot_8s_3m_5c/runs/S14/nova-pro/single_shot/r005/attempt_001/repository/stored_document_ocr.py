import boto3
from storage_client import get_textract_client

def run_ocr_on_stored_document(bucket_name, document_key):
    textract_client = get_textract_client()
    response = textract_client.start_document_text_detection(
        Document={'S3Object':{'Bucket': bucket_name, 'Name': document_key}})
    return response['JobId']

if __name__ == '__main__':
    print(run_ocr_on_stored_document('my-bucket','my-document'))