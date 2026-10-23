# [SAME-SCENARIO] select_platform_resource.py
import os
from model_client import ManagedModelClient
from model_models import DeploymentDescriptor

def select_platform_resource(project_id: str, deployment_name: str) -> DeploymentDescriptor:
    """Resolve a provider‑specific deployment resource.

    This helper loads the platform client, queries the deployment catalog, and returns a DeploymentDescriptor
    that can be used for subsequent invocations.
    """
    client = ManagedModelClient()
    # Example: using the client to fetch deployment metadata; replace with real SDK call as needed.
    deployment = client.get_deployment(project_id=project_id, deployment_name=deployment_name)
    return DeploymentDescriptor(
        deployment_id=deployment['id'],
        model_id=deployment['model_ref'],
        # any additional provider‑specific fields can be stored here
    )
