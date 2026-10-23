import os
import requests
from document_models import OcrResult

def check_content_safety(ocr_result: OcrResult) -> bool:
    """Check the extracted OCR text for unsafe or harmful material using the ibm-watsonx-ai guardrails API.
    Returns True if the content is considered safe, False otherwise.
    """
    endpoint = "https://api.us-south.text.cognize.ibm.com/v1/guardrails"
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise RuntimeError("WatsonX credentials missing")
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"project_id": project_id, "content": ocr_result.full_text}
    resp = requests.post(endpoint, json=payload, headers=headers)
    resp.raise_for_status()
    result = resp.json()
    # Assuming response contains 'safe': true/false
    return result.get('safe', False)
