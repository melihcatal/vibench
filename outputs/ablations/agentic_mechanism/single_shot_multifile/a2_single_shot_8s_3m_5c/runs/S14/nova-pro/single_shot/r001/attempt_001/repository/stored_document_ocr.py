import boto3
from storage_client import get_s3_client

def run_ocr_on_stored_document(bucket_name, document_key):
    s3_client = get_s3_client()
    document = s3_client.get_object(Bucket=bucket_name, Key=document_key)
    document_content = document['Body'].read()
    
    textract_client = boto3.client('textract')
    response = textract_client.detect_document_text(Document={'Bytes': document_content})
    
    return response

if __name__ == '__main__':
    print(run_ocr_on_stored_document('my-bucket', 'my-document-key'))