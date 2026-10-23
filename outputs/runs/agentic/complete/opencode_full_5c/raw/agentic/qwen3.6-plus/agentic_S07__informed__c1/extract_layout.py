from document_client import get_di_client, read_image_bytes, parse_di_response_to_blocks
from document_models import OCRRequest, OCRLayoutResponse, normalize_layout_response


def extract_layout_from_image(request: OCRRequest) -> OCRLayoutResponse:
    client = get_di_client()

    if request.image_path:
        image_data = read_image_bytes(request.image_path)
    elif request.image_bytes:
        image_data = request.image_bytes
    else:
        return OCRLayoutResponse(blocks=[], page_count=0)

    poller = client.begin_analyze_document(
        "prebuilt-layout",
        body=image_data,
        content_type=request.content_type,
    )
    result = poller.result()

    response = normalize_layout_response(result)
    return response


def extract_layout_from_bytes(
    image_bytes: bytes, content_type: str = "application/octet-stream"
) -> OCRLayoutResponse:
    request = OCRRequest(image_bytes=image_bytes, content_type=content_type)
    return extract_layout_from_image(request)


def extract_layout_from_file(
    image_path: str, content_type: str = "application/octet-stream"
) -> OCRLayoutResponse:
    request = OCRRequest(image_path=image_path, content_type=content_type)
    return extract_layout_from_image(request)
