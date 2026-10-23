# invoke_platform_model.py
# SAME-SCENARIO
# Invokes a provider-managed model through a project-, deployment-, or inference-profile-scoped platform client

from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse


def invoke_model(
    project_id: str, deployment_id: str, input_text: str
) -> ModelInvocationResponse:
    """Invoke the managed model platform using the configured client.

    Args:
        project_id: The provider project identifier.
        deployment_id: The deployment or model endpoint identifier.
        input_text: Prompt or input to send to the model.

    Returns:
        A ModelInvocationResponse object containing model output and provider metadata.
    """
    client = ManagedModelClient()  # Concrete provider client (e.g., OpenAI GPT-4)
    request = ModelInvocationRequest(
        project_id=project_id, deployment_id=deployment_id, input=input_text
    )
    response = client.invoke(request)  # provider-specific call
    return response
