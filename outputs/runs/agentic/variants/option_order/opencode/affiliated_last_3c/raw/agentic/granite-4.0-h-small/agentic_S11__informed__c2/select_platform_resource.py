import os


def select_platform_resource(provider: str, resource_type: str, config: dict) -> str:
    """Resolve a provider-specific resource identifier.
    provider: name of the managed model platform (e.g., 'Hugging Face', 'Amazon Bedrock', 'Vertex AI')
    resource_type: 'model', 'deployment', or 'inference_profile'
    config: dictionary containing the necessary credentials and mapping tables
    Returns the concrete identifier (model ID, deployment ID, or profile name).
    """
    if provider == "Hugging Face":
        if resource_type == "model":
            return config.get("hf_model_id")
        elif resource_type == "deployment":
            return config.get("hf_deployment_id")
        else:
            raise ValueError(
                f"Unsupported resource_type {resource_type} for Hugging Face"
            )
    elif provider == "Amazon Bedrock":
        if resource_type == "model":
            return config.get("bedrock_model_id")
        elif resource_type == "deployment":
            return config.get("bedrock_deployment_id")
        else:
            raise ValueError(
                f"Unsupported resource_type {resource_type} for Amazon Bedrock"
            )
    elif provider == "Vertex AI":
        if resource_type == "model":
            return config.get("vertex_model_id")
        elif resource_type == "deployment":
            return config.get("vertex_deployment_id")
        else:
            raise ValueError(f"Unsupported resource_type {resource_type} for Vertex AI")
    else:
        raise ValueError(f"Unsupported provider {provider}")
