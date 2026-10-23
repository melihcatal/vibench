# select_platform_resource.py
# [SAME-SCENARIO] Resolve the provider-specific model/deployment/inference resource before invocation

from model_client import ManagedModelClient
from model_models import ModelSpec, DeploymentSpec


def select_platform_resource(model_id: str, deployment_id: str = None) -> tuple[ModelSpec, DeploymentSpec]:
    """Selects and validates a model and deployment from the provider's catalog.

    Args:
        model_id: Identifier of the provider's model family (e.g., Azure OpenAI 'gpt-4o').
        deployment_id: Optional deployment name; if omitted, the client picks the default.

    Returns:
        A pair (model_spec, deployment_spec) ready for invocation.
    """
    client = ManagedModelClient()  # uses Azure OpenAI credentials from env
    model_spec = client.get_model(model_id)          # provider API call
    deployment_spec = client.get_deployment(model_id, deployment_id) if deployment_id else client.get_default_deployment(model_id)
    return model_spec, deployment_spec

if __name__ == "__main__":
    # Example: fetch info for gpt-4o with a custom deployment "my-prod-dep"
    model, deployment = select_platform_resource(model_id="gpt-4o", deployment_id="my-prod-dep")
    print(model, deployment)
