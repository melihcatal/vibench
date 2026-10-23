from openai import AzureOpenAI
import os

def get_azure_openai_client(config):
    return AzureOpenAI(
        azure_endpoint=config.get("endpoint", os.environ.get("AZURE_OPENAI_ENDPOINT")),
        api_key=config.get("api_key", os.environ.get("AZURE_OPENAI_API_KEY")),
        api_version=config.get("api_version", "2024-10-21")
    )

def get_azure_openai_deployment(config):
    return config.get("deployment", os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME"))
