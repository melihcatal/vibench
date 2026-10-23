# model_client.py
# [HELPER] Local configuration and client helper utilities for Managed Model Platform Workflow

# Concrete provider: IBM watsonx.ai

import os
from ibm_watsonx_ai import Client
from ibm_watsonx_ai.consts import ServiceType


class ModelClient:
    """Encapsulates provider-specific client creation and credential loading."""

    def __init__(self):
        # Load credentials from environment variables
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        if not self.api_key or not self.project_id:
            raise RuntimeError(
                "Please set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
            )
        # Initialize the watsonx.ai client
        self.client = Client(
            url="https://api.ibm.com/watsonx",
            api_key=self.api_key,
            service_type=ServiceType.WATSONX_AI,
        )

    def invoke(self, deployment_id, prompt):
        """Invoke a generative deployment.
        Args:
            deployment_id (str): Deployment identifier.
            prompt (str): Generation prompt.
        Returns: dict with 'output' and 'metadata' keys.
        """
        resp = self.client.generation.run(
            deployment_id=deployment_id, prompt=prompt, output_format="json"
        )
        return {
            "output": resp.text,
            "metadata": {
                "provider": "watsonx.ai",
                "deployment_id": deployment_id,
                "request_id": resp.request_id,
                "usage": resp.usage,
                "timestamp": resp.creation_date,
            },
        }


# Example usage when run directly
if __name__ == "__main__":
    client = ModelClient()
    DEPLOYMENT = "my-wx-deployment"
    PROMPT = "Explain machine learning in one sentence."
    res = client.invoke(DEPLOYMENT, PROMPT)
    print(res)
