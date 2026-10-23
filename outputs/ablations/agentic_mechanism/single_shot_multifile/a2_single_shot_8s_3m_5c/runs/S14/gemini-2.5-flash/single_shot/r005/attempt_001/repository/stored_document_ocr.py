import os
from storage_client import get_textract_client, S3_BUCKET_NAME
from storage_models import OcrDocumentRequest, OcrDocumentResponse

def run_ocr_on_stored_document(request: OcrDocumentRequest) -> OcrDocumentResponse:
    textract_client = get_textract_client()
    
    try:
        # For simplicity, using detect_document_text which works for single-page documents
        # For multi-page or larger documents, start_document_text_detection would be used asynchronously.
        response = textract_client.detect_document_text(
            Document={
                'S3Object': {
                    'Bucket': S3_BUCKET_NAME,
                    'Name': request.object_key
                }
            }
        )

        detected_text_lines = []
        for item in response.get('Blocks', []):
            if item['BlockType'] == 'LINE':
                detected_text_lines.append(item['Text'])
        
        full_text = "\n".join(detected_text_lines)

        return OcrDocumentResponse(success=True, text_content=full_text)
    except Exception as e:
        return OcrDocumentResponse(success=False, error_message=str(e))
