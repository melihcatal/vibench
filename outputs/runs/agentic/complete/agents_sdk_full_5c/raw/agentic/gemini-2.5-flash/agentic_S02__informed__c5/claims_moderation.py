import os
import requests
import json

class AzureContentSafetyModerator:
    def __init__(self, endpoint: str, key: str):
        self.endpoint = endpoint
        self.key = key
        self.api_version = "2023-10-15-preview"

    def moderate_text(self, text: str) -> dict:
        """Moderates free-text claims or notes using Azure AI Content Safety."""
        url = f"{self.endpoint}/contentsafety/text:analyze?api-version={self.api_version}"
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "categories": [
                "Hate",
                "SelfHarm",
                "Sexual",
                "Violence"
            ],
            "blocklistNames": [],
            "outputType": "FourSeverityLevels"
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_details = {"error": str(e)}
            if e.response is not None:
                try:
                    error_details["response"] = e.response.json()
                except json.JSONDecodeError:
                    error_details["response"] = e.response.text
            return error_details

if __name__ == "__main__":
    AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "YOUR_AZURE_CONTENT_SAFETY_ENDPOINT")
    AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "YOUR_AZURE_CONTENT_SAFETY_KEY")

    if AZURE_CONTENT_SAFETY_ENDPOINT == "YOUR_AZURE_CONTENT_SAFETY_ENDPOINT" or AZURE_CONTENT_SAFETY_KEY == "YOUR_AZURE_CONTENT_SAFETY_KEY":
        print("Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.")
    else:
        moderator = AzureContentSafetyModerator(AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY)

        example_claims = [
            "This is a perfectly normal user claim.",
            "I hate how slow the login is! This is infuriating.",
            "I will harm myself if I can't log in.",
            "Some sexually suggestive content here."
        ]

        print("--- Claims Moderation ---")
        for i, claim in enumerate(example_claims):
            print(f"\nClaim {i+1}: '{claim}'")
            moderation_result = moderator.moderate_text(claim)
            print(json.dumps(moderation_result, indent=2))
