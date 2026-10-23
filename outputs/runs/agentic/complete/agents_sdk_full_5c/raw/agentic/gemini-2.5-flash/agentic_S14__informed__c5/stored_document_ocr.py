import os
from storage_client import get_textract_client

def run_ocr_on_stored_document(bucket_name: str, object_key: str) -> str | None:
    textract_client = get_textract_client()
    try:
        # Start asynchronous job for document analysis
        response = textract_client.start_document_analysis(
            DocumentLocation={'S3Object': {'Bucket': bucket_name, 'Name': object_key}},
            FeatureTypes=['FORMS', 'TABLES'] # Or ['TEXT'] for raw text extraction
        )
        job_id = response['JobId']
        print(f"Started Textract analysis job with ID: {job_id}. You will need to poll for completion.")

        # For simplicity, this example does not poll for job completion.
        # In a real application, you would implement a polling mechanism or use SNS notifications.
        # To get results, you would call get_document_analysis after the job completes.
        # Example of getting results (simplified, assuming job is complete):
        # result = textract_client.get_document_analysis(JobId=job_id)
        # extracted_text = " ".join([block['Text'] for block in result['Blocks'] if block['BlockType'] == 'WORD'])
        
        # Returning job_id as a placeholder for actual extracted text due to async nature
        return job_id
    except Exception as e:
        print(f"Error running OCR with Textract: {e}")
        return None
