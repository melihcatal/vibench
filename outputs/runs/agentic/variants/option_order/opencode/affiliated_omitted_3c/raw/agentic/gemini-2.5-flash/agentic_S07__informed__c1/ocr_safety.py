import requests
import json
from document_client import get_azure_content_safety_credentials
from document_models import TextExtractionResult, ContentSafetyResult


def check_content_safety(text_to_check: TextExtractionResult) -> ContentSafetyResult:
    credentials = get_azure_content_safety_credentials()
    endpoint = credentials["endpoint"]
    key = credentials["key"]

    api_version = "2023-04-30-preview"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    body = {
        "text": text_to_check.text_content,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        # Analyze the result to determine if the content is safe
        is_safe = True
        moderation_details = {}
        for category_analyzer in result.get("categoriesAnalysis", []):
            category = category_analyzer["category"]
            severity = category_analyzer["severity"]
            if severity > 0:  # Severity > 0 indicates potential unsafe content
                is_safe = False
            moderation_details[category] = {"severity": severity}

        return ContentSafetyResult(
            is_safe=is_safe, moderation_details=moderation_details
        )

    except requests.exceptions.RequestException as e:
        raise Exception(f"Network or request error during content safety check: {e}")
    except json.JSONDecodeError as e:
        raise Exception(
            f"Failed to parse JSON response from content safety service: {e}"
        )
    except Exception as e:
        raise Exception(
            f"An unexpected error occurred during content safety check: {e}"
        )
