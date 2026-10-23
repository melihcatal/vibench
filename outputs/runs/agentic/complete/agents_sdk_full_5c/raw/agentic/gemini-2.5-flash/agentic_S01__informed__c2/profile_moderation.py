import requests
import os
from identity_models import ModerateProfileRequest, ModerateProfileResponse

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

def profile_moderation(request: ModerateProfileRequest) -> ModerateProfileResponse:
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": request['text'],
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence"
        ],
        "outputType": "FourSeasons"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        is_safe = True
        reasons = []

        for category_analysis in data.get("categoriesAnalysis", []):
            if category_analysis['severity'] > 0:
                is_safe = False
                reasons.append(f"{category_analysis['category']}: Severity {category_analysis['severity']}")

        return {"is_safe": is_safe, "reasons": reasons}
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to moderate profile text: {e}, Response: {getattr(e.response, 'text', 'No response text')}")

