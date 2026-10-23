from typing import Dict, Any
from model_client import load_config

def select_platform_resource(resource_name: str | None = None, config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Resolves a provider-specific model or deployment resource."""
    config = config or load_config()
    
    # For Azure OpenAI, the resource is primarily the deployment name.
    # We'll assume resource_name, if provided, overrides the configured default.
    deployment_name = resource_name or config.get('AZURE_OPENAI_DEPLOYMENT_NAME')
    
    if not deployment_name:
        raise ValueError("Azure OpenAI deployment name not specified in config or environment variables.")
        
    return {
        'deployment_name': deployment_name,
        'azure_endpoint': config.get('AZURE_OPENAI_ENDPOINT'),
        'api_key': config.get('AZURE_OPENAI_API_KEY'),
        'api_version': config.get('AZURE_OPENAI_API_VERSION')
    }
