import os
import requests
from security_models import AnalyzedText


def check_text_for_safety(text: str) -> AnalyzedText:
    """
    Checks secret labels for unsafe text using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError(
            "Azure Content Safety credentials are not set in environment variables."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}
    payload = {"text": text}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        is_safe = all(
            category.get("severity", 0) == 0
            for category in result.get("categoriesAnalysis", [])
        )

        return AnalyzedText(text=text, is_safe=is_safe, details=result)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred calling Azure Content Safety API: {e}")
        return AnalyzedText(text=text, is_safe=False, details={"error": str(e)})


if __name__ == "__main__":
    safe_label = "database-credentials-production"
    unsafe_label = "this is a hateful and violent secret name"

    safe_analysis = check_text_for_safety(safe_label)
    print(f"Analysis for '{safe_analysis.text}': Safe = {safe_analysis.is_safe}")

    unsafe_analysis = check_text_for_safety(unsafe_label)
    print(f"Analysis for '{unsafe_analysis.text}': Safe = {unsafe_analysis.is_safe}")
    if not unsafe_analysis.is_safe:
        print("Details:", unsafe_analysis.details)
