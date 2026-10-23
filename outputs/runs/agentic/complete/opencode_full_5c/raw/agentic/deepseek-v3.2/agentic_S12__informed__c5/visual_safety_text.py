import os
import requests
import json


def check_labels_for_unsafe_text(labels, description):
    """Check generated visual labels for unsafe text using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required"
        )

    text_to_check = f"{description}. Labels: {', '.join([label['description'] for label in labels]) if labels else 'No labels'}"

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": key}

    payload = {
        "text": text_to_check,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(
            f"Azure Content Safety API error: {response.status_code} - {response.text}"
        )

    result = response.json()

    categories_analysis = {}
    is_safe = True

    for category in result.get("categoriesAnalysis", []):
        category_name = category["category"]
        severity = category["severity"]
        categories_analysis[category_name] = severity

        if severity > 1:  # Severity levels: 0=Safe, 1=Low, 2=Medium, 3=High
            is_safe = False

    return {
        "is_safe": is_safe,
        "categories_analysis": categories_analysis,
        "text_checked": text_to_check[:200] + "..."
        if len(text_to_check) > 200
        else text_to_check,
        "provider": "Azure AI Content Safety",
    }
