import boto3
from storage_models import StoredDocumentOcrRequest, StoredDocumentOcrResponse

def get_textract_client():
    return boto3.client('textract')

def stored_document_ocr(request: StoredDocumentOcrRequest) -> StoredDocumentOcrResponse:
    textract_client = get_textract_client()

    # For simplicity, this example assumes a synchronous OCR operation for small documents.
    # For larger documents, you would typically use start_document_text_detection
    # and get_document_text_detection for an asynchronous workflow.
    response = textract_client.detect_document_text(
        Document={'S3Object': {'Bucket': request.bucket_name, 'Name': request.object_name}}
    )

    extracted_text = []
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            extracted_text.append(item['Text'])
            
    return StoredDocumentOcrResponse(extracted_text='\n'.join(extracted_text))
