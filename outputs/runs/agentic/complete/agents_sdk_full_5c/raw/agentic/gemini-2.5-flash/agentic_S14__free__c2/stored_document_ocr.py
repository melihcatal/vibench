import boto3
from storage_client import get_textract_client
from storage_models import DocumentTextractJobStatus
import time

def start_document_ocr_analysis(bucket_name: str, object_key: str) -> DocumentTextractJobStatus:
    """
    Starts an asynchronous OCR job on a stored document object in AWS Textract.
    Returns the job ID and initial status.
    """
    textract_client = get_textract_client()
    
    try:
        response = textract_client.start_document_analysis(
            DocumentLocation={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': object_key
                }
            },
            FeatureTypes=['FORMS', 'TABLES'] # Or ['TEXT'] for basic text extraction
        )
        job_id = response['JobId']
        return DocumentTextractJobStatus(job_id=job_id, status="IN_PROGRESS")
    except textract_client.exceptions.ClientError as e:
        print(f"Error starting Textract job: {e}")
        raise

def get_document_ocr_results(job_id: str) -> Dict[str, Any]:
    """
    Retrieves the results of an asynchronous OCR job from AWS Textract.
    This function is illustrative; a real-world scenario would use SNS/SQS for job completion notifications.
    """
    textract_client = get_textract_client()
    
    pages = []
    next_token = None
    
    while True:
        if next_token:
            response = textract_client.get_document_analysis(
                JobId=job_id,
                NextToken=next_token
            )
        else:
            response = textract_client.get_document_analysis(
                JobId=job_id
            )
        
        pages.append(response)
        next_token = response.get('NextToken')
        if not next_token:
            break

    # For simplicity, we're returning the raw pages. In a real app, you'd parse these.
    return {
        "job_status": response.get('JobStatus'),
        "analyze_result": pages
    }

if __name__ == '__main__':
    # Example usage (requires an S3 document and proper permissions):
    # bucket = "your-textract-input-bucket"
    # key = "your-document.pdf"
    # try:
    #     job_status = start_document_ocr_analysis(bucket, key)
    #     print(f"Started Textract job with ID: {job_status.job_id}. Status: {job_status.status}")

    #     # In a real application, you would wait for completion using SNS/SQS
    #     # For demonstration, we'll poll (not recommended for production)
    #     print("Polling for results (this might take a while)...")
    #     while job_status.status == "IN_PROGRESS":
    #         time.sleep(10) # Wait 10 seconds before polling again
    #         response = textract_client.get_document_analysis(JobId=job_status.job_id)
    #         job_status.status = response['JobStatus']
    #         print(f"Current job status: {job_status.status}")
        
    #     if job_status.status == "SUCCEEDED":
    #         results = get_document_ocr_results(job_status.job_id)
    #         # Process results here
    #         # print(results['analyze_result'][0]['Blocks'][:10]) # Print first 10 blocks
    #         print("OCR job succeeded. Results retrieved.")
    #     elif job_status.status == "FAILED":
    #         print("OCR job failed.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    pass
