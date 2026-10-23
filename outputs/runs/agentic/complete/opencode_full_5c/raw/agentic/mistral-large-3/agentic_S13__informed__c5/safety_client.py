from typing import Dict, List, Optional, Union
import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GuardrailsMetaNames


class WatsonXGuardrailsClient:
    """Client for WatsonX Guardrails HAP detection."""

    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.client = self._initialize_client()
        self.guardrails = self._initialize_guardrails()

    def _initialize_client(self) -> APIClient:
        return APIClient(
            credentials={"apikey": self.api_key}, project_id=self.project_id
        )

    def _initialize_guardrails(self) -> ModelInference:
        guardrails_params = {
            GuardrailsMetaNames.HAP: {
                "input": {"enabled": True, "threshold": 0.75, "send_tokens": False},
                "output": {"enabled": True, "threshold": 0.75},
            }
        }
        return ModelInference(
            model_id="ibm/granite-guardrails-v1",
            params=guardrails_params,
            client=self.client,
        )

    def moderate_text(self, text: str) -> Dict[str, Union[bool, float, Dict]]:
        """Moderate text for HAP content using WatsonX Guardrails."""
        response = self.guardrails.generate(text=text)
        return {
            "is_safe": not response.get("results", [{}])[0]
            .get("hap", {})
            .get("flagged", False),
            "score": response.get("results", [{}])[0].get("hap", {}).get("score", 0.0),
            "categories": response.get("results", [{}])[0]
            .get("hap", {})
            .get("categories", {}),
        }

    def moderate_batch(
        self, texts: List[str]
    ) -> List[Dict[str, Union[bool, float, Dict]]]:
        """Moderate a batch of texts for HAP content."""
        responses = self.guardrails.generate(text=texts)
        return [
            {
                "is_safe": not result.get("hap", {}).get("flagged", False),
                "score": result.get("hap", {}).get("score", 0.0),
                "categories": result.get("hap", {}).get("categories", {}),
            }
            for result in responses.get("results", [])
        ]
