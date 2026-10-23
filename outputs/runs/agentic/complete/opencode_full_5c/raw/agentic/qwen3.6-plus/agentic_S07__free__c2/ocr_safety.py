import requests
from document_client import AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY


AZURE_CONTENT_SAFETY_TEXT_API = (
    AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/") + "/contentsafety/text:analyze"
)


def check_text_safety(text: str, categories: list = None) -> dict:
    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    payload = {
        "text": text,
        "categories": categories,
        "outputType": "FourSeverityLevels",
    }
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    response = requests.post(
        AZURE_CONTENT_SAFETY_TEXT_API, headers=headers, json=payload
    )
    response.raise_for_status()
    return response.json()


def check_ocr_text_safety(ocr_text: str) -> dict:
    result = check_text_safety(ocr_text)
    return result


def is_text_safe(ocr_text: str, max_severity: int = 2) -> bool:
    result = check_text_safety(ocr_text)
    categories_analysis = result.get("categoriesAnalysis", [])
    for cat in categories_analysis:
        if cat.get("severity", 0) > max_severity:
            return False
    return True


def get_safety_summary(ocr_text: str) -> dict:
    result = check_text_safety(ocr_text)
    summary = {"blocklistsMatch": result.get("blocklistsMatch", []), "categories": {}}
    for cat in result.get("categoriesAnalysis", []):
        summary["categories"][cat["category"]] = cat.get("severity", 0)
    return summary
