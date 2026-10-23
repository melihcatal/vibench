from model_client import ManagedModelClient


def select_platform_resource(provider, resource_type, name):
    # Concrete provider: Azure OpenAI
    client = ManagedModelClient(provider="azure-openai")
    if resource_type == "model":
        return client.get_model(name)
    elif resource_type == "deployment":
        return client.get_deployment(name)
    elif resource_type == "inference_profile":
        return client.get_inference_profile(name)
    raise ValueError(f"Unknown resource type: {resource_type}")
