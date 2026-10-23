
import os
import requests
import json

class ModelClient:
    def __init__(self, api_key: str = None, api_endpoint: str = None):
        self.api_key = api_key or os.getenv("MODEL_API_KEY")
        self.api_endpoint = api_endpoint or os.getenv("MODEL_API_ENDPOINT")

        if not self.api_key:
            raise ValueError("API key not provided. Set MODEL_API_KEY environment variable or pass it to the constructor.")
        if not self.api_endpoint:
            raise ValueError("API endpoint not provided. Set MODEL_API_ENDPOINT environment variable or pass it to the constructor.")

    def predict(self, data: dict) -> dict:
        """
        Makes a prediction request to the managed model platform.

        Args:
            data: A dictionary containing the input data for the model.

        Returns:
            A dictionary containing the prediction results.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        try:
            response = requests.post(self.api_endpoint, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during prediction: {e}")
            raise
