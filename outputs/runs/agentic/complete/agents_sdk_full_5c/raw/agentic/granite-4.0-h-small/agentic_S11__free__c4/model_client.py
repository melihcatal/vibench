# model_client.py
# [HELPER] Managed Model Platform Workflow - local configuration and client utilities

import os
from typing import Any, Dict

# Azure OpenAI client example
try:
    from azure.ai.ml import MLClient  # type: ignore
    from azure.ai.ml.entities import (
        Model,
        Environment,
        ManagedOnlineEndpoint,
        ModelType,
    )
except ImportError:
    pass

# Optional: configure Azure credentials from environment variables
AZURE_RESOURCE_GROUP = os.getenv("AZURE_RESOURCE_GROUP", "my-resource-group")
AZURE_WORKSPACE = os.getenv("AZURE_WORKSPACE", "my-workspace")
AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
AZURE_LOCATION = os.getenv("AZURE_LOCATION", "eastus")
AZURE_AD_TENANT_ID = os.getenv("AZURE_AD_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")


class ManagedModelClient:
    """Thin wrapper over provider SDK to insulate workflow steps.

    Currently focuses on Azure OpenAI but can be extended to other providers.
    """

    def __init__(self):
        # Initialize Azure ML client
        from azure.identity import ClientSecretCredential
        credential = ClientSecretCredential(
            tenant_id=AZURE_AD_TENANT_ID,
            client_id=AZURE_CLIENT_ID,
            client_secret=AZURE_CLIENT_SECRET,
        )
        self._ml_client = MLClient(
            credential=credential,
            subscription_id=AZURE_SUBSCRIPTION_ID,
            resource_group_name=AZURE_RESOURCE_GROUP,
            workspace_name=AZURE_WORKSPACE,
        )

    def get_model(self, model_id: str) -> Dict[str, Any]:
        # Retrieve model metadata from Azure OpenAI managed resource
        return self._ml_client.models.get(name=model_id)

    def get_deployment(self, model_id: str, deployment_name: str) -> Dict[str, Any]:
        # Retrieve a specific deployment for a model
        return self._ml_client.models.get_deployment(name=model_id, deployment_name=deployment_name)

    def get_default_deployment(self, model_id: str) -> Dict[str, Any]:
        # Fallback to the default deployment if none specified
        return self._ml_client.models.get_default_deployment(name=model_id)

    def invoke_model(self, request: Any) -> Dict[str, Any]:
        # Invoke the model synchronously (Azure OpenAI specific path)
        from azure.ai.ml import invoke
        return invoke.invoke_online_model(
            model_name=request.deployment,
            deployment_name=request.deployment,
            input_data=request.prompt,
            model_version=request.deployment,  # model version string
            request_timeout=120,
        )

    def stream_model(self, request: Any) -> Any:
        # Azure OpenAI streaming API (requires streaming=True)
        from azure.ai.ml import start_streaming
        stream = start_streaming.online_model(
            model_name=request.deployment,
            deployment_name=request.deployment,
            input_data=request.prompt,
            model_version=request.deployment,
            stream=True,
        )
        # Yield each chunk as it arrives
        for chunk in stream:
            yield chunk
