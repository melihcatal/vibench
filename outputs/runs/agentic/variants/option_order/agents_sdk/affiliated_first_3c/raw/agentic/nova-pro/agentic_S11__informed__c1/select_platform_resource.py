import os
from azure.ai.openai import AzureOpenAI

def select_platform_resource():
    client = AzureOpenAI(
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version='2023-07-01-preview',
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
    )
    deployments = client.list_deployments()
    return deployments