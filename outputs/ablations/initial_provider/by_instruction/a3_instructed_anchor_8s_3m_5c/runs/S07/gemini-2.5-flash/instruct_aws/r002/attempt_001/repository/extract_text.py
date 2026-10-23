from document_client import get_textract_client
from document_models import DocumentInput, ExtractionResult

def extract_plain_text(document_input: DocumentInput) -> ExtractionResult:
    textract_client = get_textract_client()
    response = textract_client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': document_input.s3_bucket,
                'Name': document_input.s3_key
            }
        }
    )

    extracted_text = []
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            extracted_text.append(item['Text'])

    return ExtractionResult(text="\n".join(extracted_text), raw_response=response)
