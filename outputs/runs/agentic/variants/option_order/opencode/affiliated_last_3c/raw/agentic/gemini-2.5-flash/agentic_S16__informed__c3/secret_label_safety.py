import os
import requests
import json
from security_models import ContentSafetyRequest, ContentSafetyResponse


def check_secret_label_safety(request: ContentSafetyRequest) -> ContentSafetyResponse:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-04-30-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "text": request.text_content,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    result = response.json()

    # Extracting the severity scores for each category
    hate_score = 0.0
    self_harm_score = 0.0
    sexual_score = 0.0
    violence_score = 0.0

    for category_result in result.get("categoryScores", []):
        if category_result["category"] == "Hate":
            hate_score = category_result["severity"]
        elif category_result["category"] == "SelfHarm":
            self_harm_score = category_result["severity"]
        elif category_result["category"] == "Sexual":
            sexual_score = category_result["severity"]
        elif category_result["category"] == "Violence":
            violence_score = category_result["severity"]

    return ContentSafetyResponse(
        hate_score=hate_score,
        self_harm_score=self_harm_score,
        sexual_score=sexual_score,
        violence_score=violence_score,
    )
