import os
import requests
from typing import List, Dict, Any
from vision_models import ImageLabel, ImageDescription, ImageSafetyResult, ImageText


def check_text_safety(
    labels: List[ImageLabel],
    description: ImageDescription | None,
    detected_text: List[ImageText],
) -> List[ImageSafetyResult]:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    all_text_content = []
    if description:
        all_text_content.append(description.text)
    for label in labels:
        all_text_content.append(label.name)
    for text_item in detected_text:
        all_text_content.append(text_item.text)

    combined_text = ". ".join(all_text_content)
    if not combined_text:
        return []

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    body = {
        "text": combined_text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()  # Raise an exception for HTTP errors

    analysis_result = response.json()

    safety_results = []
    for category_analysis in analysis_result.get("categoriesAnalysis", []):
        category = category_analysis["category"]
        severity = category_analysis["severity"]
        if severity > 0:
            safety_results.append(
                ImageSafetyResult(category=category, severity=severity)
            )

    return safety_results
