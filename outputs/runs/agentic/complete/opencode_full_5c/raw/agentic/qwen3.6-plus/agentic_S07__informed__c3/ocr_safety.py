import os
import requests
from document_models import OCRTextResult


def check_ocr_safety(text_results: list[OCRTextResult]) -> list[dict]:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    safety_results = []
    for result in text_results:
        if result.text:
            payload = {
                "text": result.text,
                "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            }
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            safety_results.append(
                {
                    "page_number": result.page_number,
                    "analysis_results": data.get("categoriesAnalysis", []),
                    "blocklists_match": data.get("blocklistsMatch", []),
                }
            )
    return safety_results
