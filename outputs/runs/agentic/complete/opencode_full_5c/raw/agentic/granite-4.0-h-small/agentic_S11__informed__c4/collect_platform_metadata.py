# collect_platform_metadata.py
# [SAME-SCENARIO] returns model output together with provider platform metadata such as usage, resource IDs, or model handles

# Service: IBM watsonx.ai (example provider)
import os
from ibm_watsonx_ai import Client

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")


def collect_metadata(deployment_id: str, payload: dict):
    """Invoke watsonx.ai and return a dict containing the model output and platform metadata."""
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
    result = {
        "output": response.get("output"),
        "usage": response.get("usage", {}),
        "resource_id": response.get("resource_id"),
        "timestamp": response.get("timestamp"),
    }
    return result


# Demo usage
if __name__ == "__main__":
    deployment_id = "demo-deployment"
    payload = {"inputs": [{"text": "Hello, metadata!"}]}
    data = collect_metadata(deployment_id, payload)
    print(data)
