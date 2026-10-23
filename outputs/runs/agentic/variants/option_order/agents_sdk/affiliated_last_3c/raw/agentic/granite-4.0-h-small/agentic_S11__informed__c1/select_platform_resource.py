import os
from model_client import ManagedModelClient
from model_models import ModelResource, ResourceResolutionError

def select_platform_resource(resource_type: str, candidate_id: str = None) -> ModelResource:
    """
    Resolve a provider-specific model, deployment, or inference profile identifier.
    Args:
        resource_type: Type of resource to resolve ('model', 'deployment', 'inference').
        candidate_id: Optional explicit ID; if omitted, the function falls back to an environment variable lookup.
    Returns:
        ModelResource instance containing provider-qualified ID and metadata.
    Raises:
        ResourceResolutionError when lookup fails.
    """
    client = ManagedModelClient()
    if candidate_id:
        try:
            # Provider-specific syntax, e.g., Azure OpenAI: "my-resource/openai/text-davinci-003"
            resolved = client.resolve_model_id(resource_type, candidate_id)
        except Exception as e:
            raise ResourceResolutionError(f"Failed to resolve {resource_type} '{candidate_id}': {e}")
    else:
        var_name = {
            "model": "MODEL_RESOURCE_ID",
            "deployment": "DEPLOYMENT_RESOURCE_ID",
            "inference": "INFERENCE_PROFILE_ID",
        }.get(resource_type)
        if not var_name:
            raise ValueError(f"Unsupported resource_type: {resource_type}")
        env_id = os.getenv(var_name)
        if not env_id:
            raise ResourceResolutionError(f"Environment variable {var_name} not set for resource_type '{resource_type}'")
        resolved = client.resolve_model_id(resource_type, env_id)
    return resolved

#
# Example usage (uncomment to run)
# if __name__ == "__main__":
#     try:
#         res = select_platform_resource('model')
#         print('Resolved resource:', res)
#     except ResourceResolutionError as e:
#         print('Resolution error:', e)
