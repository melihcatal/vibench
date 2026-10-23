import os
from typing import Optional, Dict, Any
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference


class WatsonXClient:
    def __init__(self, api_key: Optional[str] = None, project_id: Optional[str] = None):
        self.api_key = api_key or os.getenv("WATSONX_API_KEY")
        self.project_id = project_id or os.getenv("WATSONX_PROJECT_ID")

        if not self.api_key:
            raise ValueError("WATSONX_API_KEY environment variable must be set")
        if not self.project_id:
            raise ValueError("WATSONX_PROJECT_ID environment variable must be set")

        self.client = APIClient(api_key=self.api_key, project_id=self.project_id)

    def get_model_inference(
        self,
        model_id: str = "ibm/granite-13b-chat-v2",
        parameters: Optional[Dict[str, Any]] = None,
    ) -> ModelInference:
        if parameters is None:
            parameters = {
                "decoding_method": "greedy",
                "max_new_tokens": 100,
                "min_new_tokens": 1,
                "temperature": 0.7,
            }

        return ModelInference(
            model_id=model_id,
            params=parameters,
            credentials={
                "apikey": self.api_key,
                "url": "https://us-south.ml.cloud.ibm.com",
            },
            project_id=self.project_id,
        )

    def list_models(self):
        return self.client.foundation_models.list()

    def get_default_parameters(self, task_type: str = "chat") -> Dict[str, Any]:
        defaults = {
            "chat": {
                "decoding_method": "greedy",
                "max_new_tokens": 100,
                "min_new_tokens": 1,
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 50,
            },
            "code": {
                "decoding_method": "greedy",
                "max_new_tokens": 200,
                "min_new_tokens": 1,
                "temperature": 0.2,
                "top_p": 0.95,
            },
            "embedding": {"truncation": "END"},
        }
        return defaults.get(task_type, defaults["chat"])


def load_config_from_env() -> Dict[str, Any]:
    config = {
        "api_key": os.getenv("WATSONX_API_KEY"),
        "project_id": os.getenv("WATSONX_PROJECT_ID"),
        "region": os.getenv("WATSONX_REGION", "us-south"),
        "api_endpoint": os.getenv(
            "WATSONX_API_ENDPOINT", "https://us-south.ml.cloud.ibm.com"
        ),
    }
    return config
