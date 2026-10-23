# [SAME-SCENARIO] select_platform_resource.py

from model_models import ManagedModelRequest, ModelCatalogEntry


def select_platform_resource(request: ManagedModelRequest):
    """Resolves a provider‑specific model, deployment, or inference resource.

    Given a generic request, this helper looks up the appropriate resource ID
    from a local catalog (e.g., environment variable mapping) and returns it.
    The catalog can be expanded to accept CLI arguments, a config file, or a
    remote registry.

    Args:
        request (ManagedModelRequest): Incoming request containing model name,
                                       deployment hint, and optional version.

    Returns:
        ModelCatalogEntry: Dict with provider‑specific fields (project,
                           deployment, etc.) ready for client invocation.
    """
    # Example local catalog using environment variables
    catalog = {
        "gemma-2b": {
            "provider": "vertex-ai",
            "project_id": "my-gcp-project",
            "deployment_id": "gemma-2b-deployment",
        },
        "claude-3.5": {
            "provider": "azure-openai",
            "endpoint": "https://my-azure-openai.openai.azure.com/openai/deployments/claude-3.5/",
            "api_key": "YOUR_AZURE_KEY_HERE",
        },
    }

    model_name = request.model_name.lower()
    entry = catalog.get(model_name)
    if not entry:
        raise ValueError(f"Model '{model_name}' not found in local catalog.")
    return ModelCatalogEntry(**entry)
