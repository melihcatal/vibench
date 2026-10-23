import os
import requests
from model_models import ModerationResult
from dotenv import load_dotenv

load_dotenv()


def check_content_safety(text: str) -> ModerationResult:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    api_version = "2023-10-01-preview"

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {"text": text}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    categories = {}
    category_scores = {}
    flagged = False

    for category_result in result.get("categoriesAnalysis", []):
        category_name = category_result["category"]
        severity = category_result["severity"]
        categories[category_name] = severity > 0
        category_scores[category_name] = (
            severity  # Azure returns severity 0-7, which can be interpreted as a score
        )
        if severity > 0:
            flagged = True

    return ModerationResult(
        categories=categories, category_scores=category_scores, flagged=flagged
    )
