import os
from model_client import ManagedModelClient
from model_models import ResourceSelector, ResourceQuery

# Azure OpenAI configuration (same-scenario reference provider)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_RESOURCE_GROUP = os.getenv("AZURE_OPENAI_RESOURCE_GROUP", "default-group")

# Mapping of provider aliases to selector functions
SELECTORS = {
    "azure_openai": _select_azure_openai,
    # Additional providers can be added here
}


def _select_azure_openai(query: ResourceQuery) -> ResourceSelector:
    """Resolve Azure OpenAI model/deployment resources for invocation.

    Args:
        query: Encapsulated query parameters (resource_type, filters).

    Returns:
        A ResourceSelector instance populated with resolved IDs.

    Example:
        query = ResourceQuery(resource_type="deployment", name_filter="my-deployment")
        selector = _select_azure_openai(query)
        selector.deployment_id  # => resolved deployment ID
    """
    # Placeholder logic - in real implementation query Azure Resource Manager API
    # or portal metadata to locate the requested resource.
    deployment_name = query.filters.get("name_filter", "default-deployment")
    model_name = query.filters.get("model_filter", "default-model")
    return ResourceSelector(
        provider="azure_openai",
        deployment_id=f"/subscriptions/{os.getenv('AZURE_SUBSCRIPTION_ID')}/resourceGroups/{AZURE_OPENAI_RESOURCE_GROUP}/providers/Microsoft.CognitiveServices/accounts/{os.getenv('AZURE_OPENAI_ACCOUNT')}/deployments/{deployment_name}",
        model_id=f"/subscriptions/{os.getenv('AZURE_SUBSCRIPTION_ID')}/resourceGroups/{AZURE_OPENAI_RESOURCE_GROUP}/providers/Microsoft.CognitiveServices/accounts/{os.getenv('AZURE_OPENAI_ACCOUNT')}/models/{model_name}",
    )


def select_resource(query: ResourceQuery) -> ResourceSelector:
    """Dispatch to the appropriate provider-specific selector.

    Args:
        query: Query parameters for the desired resource.

    Returns:
        Resolved ResourceSelector ready for use with invocation.
    """
    selector_fn = SELECTORS.get(query.provider)
    if not selector_fn:
        raise ValueError(f"Unsupported provider: {query.provider}")
    return selector_fn(query)


if __name__ == "__main__":
    # Demo query for a specific deployment named 'gpt-4'
    query = ResourceQuery(
        resource_type="deployment",
        provider="azure_openai",
        filters={"name_filter": "gpt-4"},
    )
    selector = select_resource(query)
    print(f"Resolved Azure OpenAI deployment ID: {selector.deployment_id}")
    print(f"Resolved Azure OpenAI model ID: {selector.model_id}")
