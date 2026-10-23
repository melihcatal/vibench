from document_client import get_document_intelligence_client, get_model_id
from document_models import OCRRequest, OCRResponse, normalize_text


def extract_text(image) -> OCRResponse:
    request = OCRRequest(image=image)
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        get_model_id("ocr"), document=request.to_bytes()
    )
    result = poller.result()
    text = normalize_text(getattr(result, "content", ""))
    return OCRResponse(
        text=text, raw={"model_id": get_model_id("ocr"), "result": result}
    )
