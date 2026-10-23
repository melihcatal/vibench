import os
import requests


class LogTextSafetyChecker:
    def __init__(self):
        self.api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")

    def check_text_safety(self, text: str) -> Dict[str, Any]:
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.api_key
        }
        payload = {
            "text": text
        }
        response = requests.post(
            f"{self.endpoint}/contentsafety/text:analyze",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    checker = LogTextSafetyChecker()
    result = checker.check_text_safety("This is a test message with no unsafe content.")
    print(result)