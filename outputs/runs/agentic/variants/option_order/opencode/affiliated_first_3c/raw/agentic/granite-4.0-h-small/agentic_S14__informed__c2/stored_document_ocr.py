import os
import json
from storage_client import StorageClient
from storage_models import StorageModels
from alibabacloud_ocr_api import client as ocr_client
from alibabacloud_tea_util import models as utility_models
from google.cloud import documentai_v1 as documentai

# Use Google Document AI SDK as the concrete provider for OCR on stored documents
# Authenticate via GOOGLE_APPLICATION_CREDENTIALS environment variable

# Document AI processor ID (replace with your actual processor ID)
DOCUMENT_AI_PROCESSOR_ID = os.getenv('GOOGLE_DOCUMENT_AI_PROCESSOR_ID')
# Region for your Document AI location
DOCUMENT_AI_LOCATION = 'us-central1'

# Create a Document AI client
client = documentai.DocumentProcessorServiceClient()
parent = client.location_path('us-central1')  # fixed location for v1


def stored_document_ocr(object_key: str, bucket: str = 'your-bucket-name') -> dict:
    """Run OCR on a stored document object using Google Document AI.",
    # 1. Retrieve the raw bytes of the stored object
    storage = StorageClient().get_service()
    blob = storage.get(bucket=bucket, object=object_key)
    content = blob.download_as_bytes()

    # 2. Prepare the Document AI request
    request = documentai.ProcessRequest(name=DOCUMENT_AI_PROCESSOR_ID)
    request.raw_document.content = content
    request.raw_document.mime_type = 'application/pdf'  # adjust based on file type

    # 3. Call the Document AI service
    response = client.process_document(request=request)

    # 4. Extract text from the response
    document = response.document
    text = documentai.document_to_text(document)
    return {'ocr_text': text}

# Example usage (uncomment to test)
# print(stored_document_ocr('documents/sample.pdf'))
