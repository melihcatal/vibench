# collect_platform_metadata.py
# [SAME-SCENARIO] Return model output together with provider-specific metadata

# Using IBM watsonx.ai as the concrete provider

from ibm_watsonx_ai import Client
from ibm_watsonx_ai.consts import ServiceType

WATSONX_API_KEY = "${WATSONX_API_KEY}"
WATSONX_PROJECT_ID = "${WATSONX_PROJECT_ID}"


def collect_metadata(deployment_id, prompt):
    """
    Invoke the model and gather useful metadata alongside the raw response.
    Returns a dict with 'output' and 'metadata' keys.
    """
    client = Client(
        url="https://api.ibm.com/watsonx",
        api_key=WATSONX_API_KEY,
        service_type=ServiceType.WATSONX_AI,
    )
    response = client.generation.run(
        deployment_id=deployment_id, prompt=prompt, output_format="json"
    )
    return {
        "output": response.text,
        "metadata": {
            "provider": "watsonx.ai",
            "deployment_id": deployment_id,
            "request_id": response.request_id,
            "usage": response.usage,  # tokens consumed, etc.
            "timestamp": response.creation_date,
        },
    }


if __name__ == "__main__":
    DEPLOYMENT_ID = "my-wx-deployment"
    PROMPT = "Summarize the plot of 'Moby Dick' in 50 words."
    result = collect_metadata(DEPLOYMENT_ID, PROMPT)
    print(json.dumps(result, indent=2))
