import requests
import os
import json


class PayloadSafetyClient:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

        if not self.endpoint or not self.key:
            print(
                "Azure Content Safety endpoint or key not set in environment variables."
            )
            self.available = False
        else:
            self.available = True
            # Provider-identifying signal: Azure Content Safety API hostname
            self.headers = {
                "Ocp-Apim-Subscription-Key": self.key,
                "Content-Type": "application/json",
            }
            self.api_version = "2023-10-01"  # Specify a valid API version
            self.text_analyze_url = f"{self.endpoint}/contentsafety/text:analyze?api-version={self.api_version}"

    def check_payload_safety(self, payload_text: str) -> dict:
        if not self.available:
            return {"error": "Azure Content Safety client not initialized."}

        data = {
            "text": payload_text,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "blocklistNames": [],
            "outputType": "FourSeverityLevels",
        }

        try:
            response = requests.post(
                self.text_analyze_url, headers=self.headers, json=data
            )
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Error checking content safety: {e}"}
