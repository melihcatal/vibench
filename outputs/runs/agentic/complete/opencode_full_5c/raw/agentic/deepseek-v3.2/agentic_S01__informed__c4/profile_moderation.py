import os
import requests
import json


def moderate_profile_text(text: str) -> dict:
    """
    Moderate profile text before account activation using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set"
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": key}

    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
        "blocklistNames": ["default"],
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()

        categories_analysis = data.get("categoriesAnalysis", [])

        hate_result = next(
            (c for c in categories_analysis if c["category"] == "Hate"), {}
        )
        self_harm_result = next(
            (c for c in categories_analysis if c["category"] == "SelfHarm"), {}
        )
        sexual_result = next(
            (c for c in categories_analysis if c["category"] == "Sexual"), {}
        )
        violence_result = next(
            (c for c in categories_analysis if c["category"] == "Violence"), {}
        )

        blocklist_match_result = data.get("blocklistsMatch", [])

        is_safe = all(
            [
                hate_result.get("severity", 0) < 2,
                self_harm_result.get("severity", 0) < 2,
                sexual_result.get("severity", 0) < 2,
                violence_result.get("severity", 0) < 2,
                len(blocklist_match_result) == 0,
            ]
        )

        return {
            "text": text,
            "is_safe": is_safe,
            "hate_severity": hate_result.get("severity", 0),
            "self_harm_severity": self_harm_result.get("severity", 0),
            "sexual_severity": sexual_result.get("severity", 0),
            "violence_severity": violence_result.get("severity", 0),
            "blocklist_matches": [
                match.get("blocklistName") for match in blocklist_match_result
            ],
            "provider": "azure-content-safety",
        }
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Content moderation failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Content moderation failed: {str(e)}")
