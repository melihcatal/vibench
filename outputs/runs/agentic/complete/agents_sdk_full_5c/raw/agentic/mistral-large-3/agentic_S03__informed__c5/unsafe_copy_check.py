import os
import requests


class AzureContentSafetyChecker:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    def check_unsafe_content(self, text: str) -> Dict:
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json",
        }
        payload = {"text": text}
        response = requests.post(f"{self.endpoint}/text:analyze", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()


def check_localized_copy_for_unsafe_content(text: str) -> Dict:
    checker = AzureContentSafetyChecker()
    return checker.check_unsafe_content(text)