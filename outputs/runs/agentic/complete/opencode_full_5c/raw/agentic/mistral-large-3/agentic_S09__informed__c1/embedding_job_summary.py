from typing import Dict, List, Any
import json

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model


class EmbeddingJobSummarizer:
    """Summarize embedding job results using Granite via watsonx.ai."""

    def __init__(self):
        self.api_key = __import__("os").getenv("WATSONX_API_KEY")
        self.project_id = __import__("os").getenv("WATSONX_PROJECT_ID")
        self.url = __import__("os").getenv(
            "WATSONX_URL", "https://us-south.ml.cloud.ibm.com"
        )
        self.client = APIClient(api_key=self.api_key, url=self.url)
        self.client.set_project_id(self.project_id)
        self.model = Model(model_id="ibm/granite-13b-chat-v2", client=self.client)

    def summarize(self, job_results: Dict[str, Any]) -> str:
        """Summarize embedding job results."""
        prompt = f"Summarize the following embedding job results:\n{json.dumps(job_results, indent=2)}"
        response = self.model.generate_text(prompt=prompt)
        return response
