from typing import Optional
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient

def resolve_model_deployment(
    resource_group: str,
    account_name: str,
    deployment_name: Optional[str] = None
) -> str:
    """
    Resolves an Azure OpenAI model deployment ID using Azure Cognitive Services API.
    """
    credential = DefaultAzureCredential()
    client = CognitiveServicesManagementClient(credential, os.getenv("AZURE_SUBSCRIPTION_ID"))

    deployments = client.deployments.list(resource_group_name=resource_group, account_name=account_name)
    for deployment in deployments:
        if deployment_name and deployment.name == deployment_name:
            return deployment.properties.model.name
        elif not deployment_name and deployment.properties.model:
            return deployment.properties.model.name

    raise ValueError("No valid deployment found for the given criteria.")