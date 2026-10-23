from document_client import get_azure_document_client, load_image_bytes
from document_models import OCRTextResult


def extract_text_from_image(image_path: str) -> list[OCRTextResult]:
    client = get_azure_document_client()
    image_bytes = load_image_bytes(image_path)
    poller = client.begin_analyze_document(model_id="prebuilt-read", body=image_bytes)
    result = poller.result()
    text_results = []
    for page in result.pages:
        page_text = (
            "\n".join([line.content for line in page.lines]) if page.lines else ""
        )
        text_results.append(
            OCRTextResult(text=page_text, confidence=1.0, page_number=page.page_number)
        )
    return text_results
