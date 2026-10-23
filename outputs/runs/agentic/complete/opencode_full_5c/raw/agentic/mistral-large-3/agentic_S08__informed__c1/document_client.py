import os
from typing import Optional
from mindee import Client


class DocumentClient:
    def __init__(self):
        self.mindee_api_key = os.getenv("MINDEE_API_KEY")
        if not self.mindee_api_key:
            raise ValueError("MINDEE_API_KEY environment variable not set")
        self.client = Client(api_key=self.mindee_api_key)

    def get_client(self):
        return self.client


def load_config() -> Dict[str, str]:
    config = {
        "mindee_api_key": os.getenv("MINDEE_API_KEY"),
        "confidence_threshold": os.getenv("CONFIDENCE_THRESHOLD", "0.7"),
    }
    return config
