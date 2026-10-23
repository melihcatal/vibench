import os
from typing import Optional, Dict, Any
import requests


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<resource-name>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_visual_safety_text(
    text: str,
    categories: Optional[list] = None,
) -> Dict[str, Any]:
    if not text.strip():
        return {"error": "Empty text provided"}
    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    payload = {"text": text}
    if categories:
        payload["categories"] = categories
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    return result


def is_text_safe(
    text: str,
    threshold: int = 2,
) -> bool:
    result = check_visual_safety_text(text)
    if "error" in result:
        return True
    for category_result in result.get("categoriesAnalysis", []):
        if category_result.get("severity", 0) >= threshold:
            return False
    return True


if __name__ == "__main__":
    sample = "A beautiful sunset over the ocean with calm waters."
    result = check_visual_safety_text(sample)
    print(result)
    print(f"Safe: {is_text_safe(sample)}")
