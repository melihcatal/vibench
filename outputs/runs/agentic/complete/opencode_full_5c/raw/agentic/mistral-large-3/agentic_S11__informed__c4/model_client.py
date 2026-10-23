from typing import Optional, Dict, Any
import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames


class WatsonXModelClient:
    """
    Client for invoking IBM watsonx.ai managed models.
    Requires WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables.
    """

    def __init__(self, model_id: str = "mistralai/mistral-large-latest"):
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.model_id = model_id
        self.client = self._initialize_client()
        self.model = self._initialize_model()

    def _initialize_client(self) -> APIClient:
        return APIClient(
            credentials={
                "apikey": self.api_key,
                "url": "https://us-south.ml.cloud.ibm.com",
            }
        )

    def _initialize_model(self) -> Model:
        return Model(
            model_id=self.model_id,
            params={GenTextParamsMetaNames.PROJECT_ID: self.project_id},
            client=self.client,
        )

    def invoke(
        self, prompt: str, parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if parameters is None:
            parameters = {}

        model_params = {
            GenTextParamsMetaNames.DECODING_METHOD: parameters.get(
                "decoding_method", "greedy"
            ),
            GenTextParamsMetaNames.MAX_NEW_TOKENS: parameters.get(
                "max_new_tokens", 200
            ),
            GenTextParamsMetaNames.MIN_NEW_TOKENS: parameters.get("min_new_tokens", 0),
            GenTextParamsMetaNames.TEMPERATURE: parameters.get("temperature", 0.7),
        }

        response = self.model.generate(prompt=prompt, params=model_params)
        return {
            "results": response["results"],
            "model_id": self.model_id,
            "provider": "watsonx.ai",
        }
