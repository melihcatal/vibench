# invoke_platform_model.py
# [SAME-SCENARIO] Invoke a provider-managed model using a concrete provider

# Using IBM watsonx.ai as the concrete provider
from ibm_watsonx_ai import Client
from ibm_watsonx_ai.consts import ServiceType

# Load credentials from environment
WATSONX_API_KEY = "${WATSONX_API_KEY}"
WATSONX_PROJECT_ID = "${WATSONX_PROJECT_ID}"


def invoke_model(deployment_id, prompt):
    """Invoke the watsonx.ai generative model deployment.

    Args:
        deployment_id (str): The deployment identifier.
        prompt (str): The generation prompt.
    """
    client = Client(
        url="https://api.ibm.com/watsonx",  # base URL for watsonx.ai
        api_key=WATSONX_API_KEY,
        service_type=ServiceType.WATSONX_AI,
    )
    model_id = deployment_id  # Deployment ID doubles as model identifier
    response = client.generation.run(
        deployment_id=model_id, prompt=prompt, output_format="json"
    )
    # Return both model output and provider metadata
    return {
        "output": response.text,
        "metadata": {
            "provider": "watsonx.ai",
            "request_id": response.request_id,
            "usage": response.usage,
        },
    }


if __name__ == "__main__":
    # Example usage (credentials must be set in the environment)
    DEPLOYMENT_ID = "my-wx-deployment"
    PROMPT = "Explain the concept of quantum computing in simple terms."
    result = invoke_model(DEPLOYMENT_ID, PROMPT)
    print(result)
