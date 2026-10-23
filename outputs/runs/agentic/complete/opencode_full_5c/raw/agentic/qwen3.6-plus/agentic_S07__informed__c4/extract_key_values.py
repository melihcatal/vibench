from document_client import process_document
from document_models import build_ocr_result, OcrResult, KeyValue


def extract_key_values_from_image(
    file_bytes: bytes, mime_type: str = "image/png"
) -> OcrResult:
    document = process_document(file_bytes, mime_type=mime_type)
    result = build_ocr_result(document)
    return result


def extract_key_values_from_file(
    file_path: str, mime_type: str = "image/png"
) -> OcrResult:
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    return extract_key_values_from_image(file_bytes, mime_type=mime_type)


def get_key_values(result: OcrResult) -> list:
    return result.key_values


def get_key_values_as_dict(result: OcrResult) -> dict:
    return {kv.key: kv.value for kv in result.key_values if kv.key}
