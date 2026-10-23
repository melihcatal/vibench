# invoke_platform_model.py
# [SAME-SCENARIO] Invoke a provider-managed model using the Azure OpenAI service

from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse

def invoke_platform_model(
    deployment_name: str,
    prompt: str,
    temperature: float = 0.7,
) -> ModelInvocationResponse:
    """Invokes the Azure OpenAI model and returns the response.

    Args:
        deployment_name: Azure OpenAI deployment identifier.
        prompt: Input text for the model.
        temperature: Sampling temperature.
    """
    client = ManagedModelClient()  # configured for Azure OpenAI
    request = ModelInvocationRequest(
        deployment=deployment_name,
        prompt=prompt,
        temperature=temperature,
    )
    response = client.invoke_model(request)  # provider-specific call
    return response

if __name__ == "__main__":
    # Example usage
    out = invoke_platform_model(deployment_name="gpt-4o", prompt="Hello world")
    print(out)