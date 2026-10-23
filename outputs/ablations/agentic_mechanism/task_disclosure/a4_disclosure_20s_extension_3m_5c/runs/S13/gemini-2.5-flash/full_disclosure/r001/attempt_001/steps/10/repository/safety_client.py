
import os
import requests

class TextContentSafetyClient:
    """
    A client for interacting with the Text Content Safety API.
    """

    def __init__(self, api_key: str = None, api_endpoint: str = None):
        """
        Initializes the TextContentSafetyClient with API key and endpoint.
        """
        self.api_key = api_key or os.getenv("TEXT_CONTENT_SAFETY_API_KEY")
        self.api_endpoint = api_endpoint or os.getenv("TEXT_CONTENT_SAFETY_API_ENDPOINT", "https://api.example.com/safety")

        if not self.api_key:
            raise ValueError("API key must be provided or set as TEXT_CONTENT_SAFETY_API_KEY environment variable.")
        if not self.api_endpoint:
            raise ValueError("API endpoint must be provided or set as TEXT_CONTENT_SAFETY_API_ENDPOINT environment variable.")

    def analyze_text(self, text: str) -> dict:
        """
        Sends text to the Text Content Safety API for analysis.
        """
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }
        payload = {
            "text": text
        }
        try:
            response = requests.post(self.api_endpoint + "/analyze", headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Text Content Safety API: {e}")
            raise
