# invoke_platform_model.py
# [SAME-SCENARIO] invokes a provider-managed model through a project-, deployment-, or inference-profile-scoped platform client

# Service: IBM watsonx.ai (example provider)
import os
from ibm_watsonx_ai import Client  # provider-specific SDK import

# Configuration (environment variables)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")


def invoke_model(deployment_id: str, payload: dict):
    """Invoke the watsonx.ai generative model deployment and return the raw response."""
    client = Client(
        url="https://api.watsonx.ibm.com",
        api_key=WATSONX_API_KEY,
        project_id=WATSONX_PROJECT_ID,
    )
    response = client.api.invoke_deployment(
        deployment_id=deployment_id,
        data=payload,
        wait=True,
    )
    return response


if __name__ == "__main__":
    # Example usage
    deployment_id = "my-deployment-123"
    payload = {"inputs": [{"text": "Hello, world!"}]}
    result = invoke_model(deployment_id, payload)
    print(result)
