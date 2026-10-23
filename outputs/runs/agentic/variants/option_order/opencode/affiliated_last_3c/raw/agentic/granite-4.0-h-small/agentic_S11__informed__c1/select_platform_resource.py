import json
from model_client import ManagedModelClient
from model_models import Model, Deployment, ModelCatalog


def select_model(
    catalog: ModelCatalog,
    logical_name: str,
    target_deployment: str,
) -> Model | None:
    """Resolve a logical model identifier to a concrete deployment.

    Args:
        catalog: ModelCatalog containing project deployments.
        logical_name: Human‑readable model name (e.g., "gpt-4").
        target_deployment: Deployment name to use (e.g., "default").

    Returns:
        Model instance if found, otherwise None.
    """
    deployment = catalog.get_deployment(target_deployment)
    if not deployment:
        raise ValueError(f"Deployment '{target_deployment}' not found in catalog")
    return Model(
        model_id=logical_name,
        provider=deployment.name,
        deployment=deployment.resolve(logical_name),
    )
