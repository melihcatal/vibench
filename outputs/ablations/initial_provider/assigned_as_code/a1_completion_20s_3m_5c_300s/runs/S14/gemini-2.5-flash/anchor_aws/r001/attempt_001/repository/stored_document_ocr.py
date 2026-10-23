from storage_client import get_textract_client
from storage_models import OCRResult


def run_ocr_on_stored_document(bucket_name: str, object_name: str, config: dict = None) -> OCRResult:
    config = config or {}
    textract_client = get_textract_client(region_name=config.get("region"))
    response = textract_client.detect_document_text(
        Document={'S3Object': {'Bucket': bucket_name, 'Name': object_name}}
    )
    extracted_text = []
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            extracted_text.append(item['Text'])
    return OCRResult(text="\n".join(extracted_text))
