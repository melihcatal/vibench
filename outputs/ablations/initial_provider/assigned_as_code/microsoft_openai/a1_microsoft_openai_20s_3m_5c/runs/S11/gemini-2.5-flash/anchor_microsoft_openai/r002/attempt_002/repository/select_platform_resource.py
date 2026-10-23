from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import os


def select_platform_resource(resource_name, config=None):
    config = config or {}
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", config.get("subscription_id"))
    resource_group = os.environ.get("AZURE_RESOURCE_GROUP", config.get("resource_group"))
    workspace_name = os.environ.get("AZURE_ML_WORKSPACE_NAME", config.get("workspace_name"))

    if not all([subscription_id, resource_group, workspace_name]):
        raise ValueError("Azure subscription ID, resource group, and workspace name must be provided.")

    ml_client = MLClient(
        DefaultAzureCredential(), subscription_id, resource_group, workspace_name
    )

    try:
        # Assuming resource_name refers to a model deployment
        endpoint = ml_client.online_endpoints.get(name=resource_name)
        return {"resource_id": endpoint.id, "resource_name": endpoint.name, "resource_type": "online_endpoint"}
    except Exception as e:
        print(f"Could not find online endpoint: {e}. Trying as model...")
        try:
            model = ml_client.models.get(name=resource_name)
            return {"resource_id": model.id, "resource_name": model.name, "resource_type": "model"}
        except Exception as e:
            raise ValueError(f"Could not resolve resource '{resource_name}' as an online endpoint or model: {e}")
