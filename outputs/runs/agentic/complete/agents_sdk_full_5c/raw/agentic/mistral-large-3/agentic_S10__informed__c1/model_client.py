import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference
from typing import Optional


class WatsonXClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WatsonXClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.api_key = os.getenv("WATSONX_API_KEY")
        if not self.api_key:
            raise ValueError("WATSONX_API_KEY environment variable must be set")
        
        self.client = APIClient(credentials={"apikey": self.api_key})
        self.text_client = ModelInference(self.client)


def get_watsonx_client() -> WatsonXClient:
    return WatsonXClient()