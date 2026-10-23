import os
from typing import Optional, Dict, Any
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from model_models import WatsonXRequest, WatsonXResponse


class WatsonXClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WatsonXClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        api_key = os.getenv("WATSONX_API_KEY")
        project_id = os.getenv("WATSONX_PROJECT_ID")
        url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

        if not api_key or not project_id:
            raise ValueError(
                "WATSONX_API_KEY and WATSONX_PROJECT_ID must be set in environment variables"
            )

        self.credentials = Credentials(api_key, url=url)
        self.project_id = project_id
        self.client = ModelInference(
            model_id="",  # Model ID is set per-request
            credentials=self.credentials,
            project_id=self.project_id,
        )

    def generate(self, request: WatsonXRequest) -> WatsonXResponse:
        """Generate text using the WatsonX model."""
        response = self.client.generate(
            prompt=request.input, model_id=request.model_id, params=request.params
        )
        return WatsonXResponse(output=response["results"][0]["generated_text"])

    def generate_stream(self, request: WatsonXRequest) -> Iterator[str]:
        """Stream text generation using the WatsonX model."""
        for chunk in self.client.generate_stream(
            prompt=request.input, model_id=request.model_id, params=request.params
        ):
            yield chunk["results"][0]["generated_text"]


def get_watsonx_client() -> WatsonXClient:
    """Get or create the WatsonX client instance."""
    return WatsonXClient()
