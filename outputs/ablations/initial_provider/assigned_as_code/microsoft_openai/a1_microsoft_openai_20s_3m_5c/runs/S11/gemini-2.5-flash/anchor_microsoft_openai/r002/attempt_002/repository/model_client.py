from openai import AzureOpenAI
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import os

def get_azure_openai_client(config):
    return AzureOpenAI(
        azure_endpoint=config['endpoint'],
        api_key=config['api_key'],
        api_version=config.get('api_version', '2024-10-21')
    )

def get_azure_ml_client(config):
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", config.get("subscription_id"))
    resource_group = os.environ.get("AZURE_RESOURCE_GROUP", config.get("resource_group"))
    workspace_name = os.environ.get("AZURE_ML_WORKSPACE_NAME", config.get("workspace_name"))

    if not all([subscription_id, resource_group, workspace_name]):
        raise ValueError("Azure subscription ID, resource group, and workspace name must be provided.")

    return MLClient(
        DefaultAzureCredential(), subscription_id, resource_group, workspace_name
    )
