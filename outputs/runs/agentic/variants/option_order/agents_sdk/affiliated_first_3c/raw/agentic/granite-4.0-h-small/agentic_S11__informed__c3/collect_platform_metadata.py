from model_client import ManagedModelClient
from model_models import ModelRequest, ModelResponse

def collect_platform_metadata(deployment_name: str, prompt: str) -> ModelResponse:
    """Invoke a managed model and return both output and platform metadata.

    Args:
        deployment_name: Identifier of the deployment/model to invoke.
        prompt: Input text for the model.

    Returns:
        A ModelResponse object containing 'output' and 'metadata' fields.
    """
    client = ManagedModelClient()
    request = ModelRequest(deployment=deployment_name, prompt=prompt)
    response = client.invoke_model(request)
    # response.metadata includes usage, resource IDs, timestamps, etc., specific to the provider
    return response
