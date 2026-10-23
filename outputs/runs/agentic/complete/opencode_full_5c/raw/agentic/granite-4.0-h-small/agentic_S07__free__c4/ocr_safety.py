from document_client import DocumentClient
from document_models import SafetyCheckRequest, SafetyCheckResponse
from transformers import pipeline

def check_safety(text: str) -> SafetyCheckResponse:
    """Run a safety/content moderation check on OCR output using a HuggingFace toxicity classifier.",
    classifier = pipeline("text-classification", model="finiteautomata/badwords")
    results = classifier(text)
    flagged = [r['label'] for r in results if r['score'] > 0.9]
    return SafetyCheckResponse(
        is_safe=len(flagged) == 0,
        flagged_categories=flagged
    )


def safety_check_document(image_path: str) -> SafetyCheckResponse:
    """Extract text via OCR and immediately run safety check.",
    client = DocumentClient(service="azure_ocr")
    with open(image_path, "rb") as img:
        ocr_result = client.ocr_image(image_bytes=img.read())
        text = ocr_result.get("text", "")
    return check_safety(text)
