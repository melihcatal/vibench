from document_client import process_document
from document_models import build_ocr_result, OcrResult, LayoutElement


def extract_layout_from_image(
    file_bytes: bytes, mime_type: str = "image/png"
) -> OcrResult:
    document = process_document(file_bytes, mime_type=mime_type)
    result = build_ocr_result(document)
    return result


def extract_layout_from_file(file_path: str, mime_type: str = "image/png") -> OcrResult:
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    return extract_layout_from_image(file_bytes, mime_type=mime_type)


def get_layout_elements_by_type(result: OcrResult, element_type: str) -> list:
    return [
        elem for elem in result.layout_elements if elem.element_type == element_type
    ]


def get_all_layout_elements(result: OcrResult) -> list:
    return result.layout_elements
