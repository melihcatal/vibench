import json
from model_client import ManagedModelClient
from model_models import ModelRequest, ModelResponse

def invoke_platform_model(deployment_name: str, prompt: str) -> None:
    """Invoke a managed model using the provider-specific client and print the response.

    Args:
        deployment_name: Identifier of the deployment / model to invoke.
        prompt: Input text for the model.
    """
    client = ManagedModelClient()
    request = ModelRequest(
        deployment=deployment_name,
        prompt=prompt,
        # Optional: any provider-specific parameters can be added here
    )
    response = client.invoke_model(request)
    # response is a ModelResponse object that contains both model output and metadata
    print(json.dumps({
        "output": response.output,
        "metadata": response.metadata,
    }, indent=2))