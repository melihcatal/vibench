import os
import requests
from typing import Dict, Any

def check_content_safety(text: str) -> Dict[str, Any]:
    """Checks text content for unsafe content using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "categories": [
            "Hate",
            "Sexual",
            "SelfHarm",
            "Violence"
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors
        result = response.json()

        # Basic safety check: if any category has a high severity
        is_safe = True
        moderation_scores = {}
        if result.get("categoriesAnalysis"):
            for category_analysis in result["categoriesAnalysis"]:
                category_name = category_analysis["category"]
                severity = category_analysis["severity"]
                moderation_scores[category_name] = severity
                # Severity 0: Safe, 2: Low, 4: Medium, 6: High
                if severity >= 4: # Considering medium or high severity as unsafe
                    is_safe = False

        return {"is_safe": is_safe, "moderation_scores": moderation_scores, "raw_response": result}

    except requests.exceptions.RequestException as e:
        print(f"Error checking content safety: {e}")
        return {"is_safe": False, "moderation_scores": {}, "error": str(e)}

if __name__ == '__main__':
    # Example usage (set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY env vars)
    # text_to_check = "I hate you so much, I want to hurt you."
    # safety_result = check_content_safety(text_to_check)
    # print(safety_result)
    pass
