import json
import requests
from safety_client import (
    AWS_COMPREHEND_ENDPOINT,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
)
from safety_models import SafetyRequest, SafetyResponse, normalize_response


def moderate_text(text: str) -> SafetyResponse:
    url = f"https://{AWS_COMPREHEND_ENDPOINT}"
    headers = {
        "Content-Type": "application/x-amz-json-1.1",
        "X-Amz-Target": "Comprehend_20171127.DetectSentiment",
    }
    payload = {"Text": text, "LanguageCode": "en"}
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload),
        auth=(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY),
    )
    return normalize_response(response.json())
