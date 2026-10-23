import boto3

def run_ocr(bucket_name, document_key):
    textract_client = boto3.client('textract')
    response = textract_client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': document_key
            }
        }
    )
    return response