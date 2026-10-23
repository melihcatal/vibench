import os
import requests
import json
from security_client import get_azure_content_safety_config
from security_models import SecretLabelSafetyReport


def check_label_safety(secret_name: str, label: str) -> SecretLabelSafetyReport:
    endpoint, key = get_azure_content_safety_config()
    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint or key not configured.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    data = {"text": label}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        # Assuming a simple check for safety. Adjust based on actual API response structure.
        # This is a simplified example; actual safety check would involve iterating through categories and severities.
        is_safe = True
        safety_details = ""
        if "categoriesAnalysis" in result:
            for category_analysis in result["categoriesAnalysis"]:
                if (
                    category_analysis["severity"] > 0
                ):  # Assuming severity > 0 means unsafe
                    is_safe = False
                    safety_details += f"{category_analysis['category']}: Severity {category_analysis['severity']}. "

        if not safety_details:  # If no explicit details, state general safety
            safety_details = (
                "No immediate safety concerns detected based on configured categories."
            )

        return SecretLabelSafetyReport(
            secret_name=secret_name,
            label=label,
            is_safe=is_safe,
            safety_details=safety_details.strip(),
        )
    except requests.exceptions.RequestException as e:
        return SecretLabelSafetyReport(
            secret_name=secret_name,
            label=label,
            is_safe=False,
            safety_details=f"Error communicating with Azure Content Safety: {e}",
        )
    except Exception as e:
        return SecretLabelSafetyReport(
            secret_name=secret_name,
            label=label,
            is_safe=False,
            safety_details=f"An unexpected error occurred: {e}",
        )
