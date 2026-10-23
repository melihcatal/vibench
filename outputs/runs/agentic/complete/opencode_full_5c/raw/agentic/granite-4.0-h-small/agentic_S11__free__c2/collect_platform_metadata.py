from model_client import ManagedModelClient


def collect_platform_metadata(provider, model_id=None, deployment_id=None):
    # Concrete provider: Cohere (Command R)
    client = ManagedModelClient(provider="cohere")
    metadata = client.metadata(model_id=model_id, deployment_id=deployment_id)
    return metadata
