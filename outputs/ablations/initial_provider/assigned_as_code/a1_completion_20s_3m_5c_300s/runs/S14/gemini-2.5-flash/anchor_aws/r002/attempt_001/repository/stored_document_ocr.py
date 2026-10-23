import boto3
from storage_client import get_textract_client
from storage_models import StoredDocumentOcrRequest

def run_ocr_on_stored_document(payload: StoredDocumentOcrRequest, config: dict = None) -> dict:
    config = config or {}
    textract_client = get_textract_client(config)
    
    response = textract_client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': config["bucket"],
                'Name': payload.object_name
            }
        }
    )
    
    return {"job_id": response["JobId"]}
