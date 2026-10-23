import boto3
import json

def perform_ocr_on_stored_document(bucket_name, document_key):
    textract_client = boto3.client('textract')
    response = textract_client.start_document_text_detection(Document={'S3Object':{'Bucket': bucket_name,'Name': document_key}})
    job_id = response['JobId']
    while True:
        response = textract_client.get_document_text_detection(JobId=job_id)
        if response['JobStatus'] in ['SUCCEEDED', 'FAILED']:
            break
    return json.dumps(response, indent=4)