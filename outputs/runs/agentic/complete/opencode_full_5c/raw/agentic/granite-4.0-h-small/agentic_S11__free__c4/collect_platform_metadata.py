# collect_platform_metadata.py
# SAME-SCENARIO
# Returns model output together with provider platform metadata such as usage, resource IDs, or model handles

from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationWithMetadata


def collect_metadata(project_id: str, deployment_id: str, input_text: str):
    """
    Invoke the model and collect usage-related platform metadata.

    Args:
        project_id: Provider project identifier.
        deployment_id: Deployment or model endpoint identifier.
        input_text: Prompt or input to the model.

    Returns:
        ModelInvocationWithMetadata containing both output and metadata dict.
    """
    client = ManagedModelClient()  # concrete provider client (e.g., Google Vertex AI)
    request = ModelInvocationRequest(
        project_id=project_id, deployment_id=deployment_id, input=input_text
    )
    response = client.invoke_with_metadata(request)  # request that includes usage/IDs
    return response
