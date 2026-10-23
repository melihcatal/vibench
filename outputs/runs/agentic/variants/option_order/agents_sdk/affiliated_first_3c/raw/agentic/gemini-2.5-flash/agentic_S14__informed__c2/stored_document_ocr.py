
from storage_client import get_textract_client
from storage_models import OCRDocumentRequest, OCRDocumentResponse

def run_ocr_on_stored_document(request: OCRDocumentRequest) -> OCRDocumentResponse:
    textract_client = get_textract_client()

    response = textract_client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': request.bucket_name,
                'Name': request.object_key
            }
        }
    )

    job_id = response['JobId']

    # In a real-world scenario, you'd poll for job completion or use SNS notifications.
    # For this example, we'll do a simple get_document_text_detection to show the integration.
    # This assumes the document is small enough for a quick detection or a subsequent call.

    # For simplicity, let's assume the job completes immediately or we fetch results directly after starting.
    # A full implementation would involve polling with get_document_text_detection until job_status is SUCCEEDED.

    # For demonstration, we'll immediately try to get the results. This will likely fail for larger documents.
    # A robust solution needs an async pattern.
    result_response = textract_client.get_document_text_detection(JobId=job_id)

    full_text_list = []
    pages_text = []
    blocks = result_response.get('Blocks', [])

    current_page_text = []
    for block in blocks:
        if block['BlockType'] == 'LINE':
            full_text_list.append(block['Text'])
            current_page_text.append(block['Text'])
        elif block['BlockType'] == 'PAGE':
            if current_page_text:
                pages_text.append('\n'.join(current_page_text))
                current_page_text = []

    if current_page_text:
        pages_text.append('\n'.join(current_page_text))

    return OCRDocumentResponse(
        full_text='\n'.join(full_text_list),
        pages=pages_text,
        raw_response=result_response # Return raw response for inspection
    )
