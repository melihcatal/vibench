from typing import Dict, Any
import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model


class TextSafetyChecker:
    def __init__(self) -> None:
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.client = APIClient(api_key=self.api_key, project_id=self.project_id)
        self.model_id = "ibm/granite-guardrails-v1"

    def check_text_safety(self, text: str) -> Dict[str, Any]:
        prompt = (
            f"Check the following text for harmful, abusive, or unsafe content: {text}"
        )

        model = Model(self.model_id, self.client)
        response = model.generate_text(prompt=prompt, max_new_tokens=50)

        return {"is_safe": "harmful" not in response.lower(), "response": response}
