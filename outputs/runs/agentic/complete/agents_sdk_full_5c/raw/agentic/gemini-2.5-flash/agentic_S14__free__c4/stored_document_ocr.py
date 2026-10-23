from typing import Optional, List
from dataclasses import dataclass
from storage_client import get_textract_client

@dataclass
class StoredDocumentOcrRequest:
    bucket_name: str
    object_key: str
    feature_types: List[str] # e.g., ["FORMS", "TABLES", "SIGNATURES"]

@dataclass
class StoredDocumentOcrResponse:
    success: bool
    message: str
    job_id: Optional[str] = None
    detected_text: Optional[str] = None # For synchronous calls, if applicable
    # More detailed Textract output can be parsed from job results

def run_ocr_on_stored_document(
    request: StoredDocumentOcrRequest
) -> StoredDocumentOcrResponse:
    """
    Runs OCR on a stored document object in AWS S3 using AWS Textract.
    Initiates an asynchronous Textract job.
    """
    textract_client = get_textract_client()

    try:
        # Textract's StartDocumentTextDetection or StartDocumentAnalysis are asynchronous
        # We'll use StartDocumentAnalysis for broader capabilities (FORMS, TABLES)
        response = textract_client.start_document_analysis(
            DocumentLocation={
                'S3Object': {
                    'Bucket': request.bucket_name,
                    'Name': request.object_key
                }
            },
            FeatureTypes=request.feature_types
        )

        job_id = response.get("JobId")

        return StoredDocumentOcrResponse(
            success=True,
            message=f"Textract document analysis job started successfully. Job ID: {job_id}",
            job_id=job_id
        )
    except Exception as e:
        return StoredDocumentOcrResponse(success=False, message=f"Error starting Textract job: {str(e)}")
