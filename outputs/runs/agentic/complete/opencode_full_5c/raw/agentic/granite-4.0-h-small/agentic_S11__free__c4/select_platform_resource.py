# select_platform_resource.py
# SAME-SCENARIO
# Resolves a provider-specific model, deployment, or inference resource before invocation

from typing import Optional, Dict
from model_client import ManagedModelClient
from model_models import ResourceSpec, ResourceLookupResult


def resolve_resource(
    project_id: str,
    resource_type: str,
    identifier: str,
    config: Optional[Dict] = None,
) -> ResourceLookupResult:
    """
    Resolve a concrete provider-specific resource identifier.

    Args:
        project_id: Provider project identifier.
        resource_type: Type of resource ('model', 'deployment', 'inference').
        identifier: Human-readable name or slug of the resource.
        config: Optional extra lookup parameters (e.g., version, region).

    Returns:
        A ResourceLookupResult containing the provider's resolved resource spec.
    """
    client = ManagedModelClient()  # concrete provider client (e.g., Anthropic Claude)
    spec = ResourceSpec(
        project_id=project_id, type=resource_type, name=identifier, **(config or {})
    )
    result = client.lookup_resource(spec)  # provider-specific resolution
    return result
