import os
from typing import Optional
import requests
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

class WatsonXGuardrailsClient:
    """Client for WatsonX.ai HAP detection and guardrails."""

    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.credentials = Credentials(
            api_key=self.api_key,
            url="https://us-south.ml.cloud.ibm.com"
        )
        self.client = ModelInference(
            model_id="ibm/granite-guardrails-v1",
            params={"decoding_method": "greedy"},
            credentials=self.credentials,
            project_id=self.project_id
        )

    def analyze_text(self, text: str) -> dict:
        """Analyze text for harmful content using WatsonX guardrails."""
        response = self.client.generate(
            prompt=f"Analyze the following text for harmful content:\n\n{text}",
            params={"max_new_tokens": 100}
        )
        return response


def get_watsonx_client() -> WatsonXGuardrailsClient:
    """Factory for WatsonX guardrails client."""
    return WatsonXGuardrailsClient()