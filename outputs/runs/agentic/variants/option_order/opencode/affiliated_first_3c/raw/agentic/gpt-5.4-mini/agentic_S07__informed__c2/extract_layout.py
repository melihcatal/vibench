from document_client import get_document_intelligence_client, get_model_id
from document_models import OCRRequest


def extract_layout(image):
    request = OCRRequest(image=image)
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        get_model_id("layout"), document=request.to_bytes()
    )
    result = poller.result()
    return {
        "model_id": get_model_id("layout"),
        "pages": getattr(result, "pages", []),
        "paragraphs": getattr(result, "paragraphs", []),
        "tables": getattr(result, "tables", []),
        "raw": result,
    }
