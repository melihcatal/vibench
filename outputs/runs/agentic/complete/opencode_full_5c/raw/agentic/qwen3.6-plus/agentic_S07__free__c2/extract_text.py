from document_client import get_document_analysis_client, load_image_bytes
from document_models import OcrResult, normalize_ocr_response


AZURE_OCR_MODEL_ID = "prebuilt-read"


def extract_text_from_image(image_path: str) -> OcrResult:
    client = get_document_analysis_client()
    image_bytes = load_image_bytes(image_path)
    poller = client.begin_analyze_document(
        model_id=AZURE_OCR_MODEL_ID, document=image_bytes
    )
    result = poller.result()
    return normalize_ocr_response(result)


def extract_text_from_bytes(image_bytes: bytes) -> OcrResult:
    client = get_document_analysis_client()
    poller = client.begin_analyze_document(
        model_id=AZURE_OCR_MODEL_ID, document=image_bytes
    )
    result = poller.result()
    return normalize_ocr_response(result)


def extract_text_as_string(image_path: str) -> str:
    ocr_result = extract_text_from_image(image_path)
    return ocr_result.get_full_text()
