import os
import requests

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<resource-name>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
API_VERSION = "2024-02-15-preview"


def check_message_safety(text: str) -> dict:
    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze?api-version={API_VERSION}"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    body = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    result = response.json()
    categories = result.get("categoriesAnalysis", [])
    flagged = [c for c in categories if c.get("severity", 0) > 0]
    return {
        "safe": len(flagged) == 0,
        "categories": {c["category"]: c.get("severity", 0) for c in categories},
        "flagged_categories": [c["category"] for c in flagged],
        "raw_response": result,
    }


def check_payload_safety(payload: dict) -> dict:
    text = " ".join(str(v) for v in payload.values() if isinstance(v, str))
    if not text:
        text = str(payload)
    return check_message_safety(text)
